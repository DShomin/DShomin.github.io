---
layout: post
title:  "Langgraph Studio 가이드"
date:   2025-03-31 13:42:00 +0900
categories: LLM Langgraph
tags: Langgraph-Studio Langgraph debug
---

> 최근 Langgraph Studio 업데이트를 통해 더 이상 macOS에 국한되지 않고 모든 OS 환경에서 구동할 수 있게 되었습니다. 이 글에서는 Langgraph Studio가 왜 필요한지, 주요 기능은 무엇인지 소개하고 스튜디오 설치 및 설정 방법을 자세히 안내합니다.


## Langgraph Studio, 왜 필요할까요?
Langgraph로 만든 앱을 디버깅하는 상황을 가정해 봅시다. 질문이나 입력값을 넣고 출력값을 확인하기 위한 별도의 스크립트나 화면 구성이 필요할 것입니다. 워크플로우 중간의 값을 확인하려면 추가적인 처리 과정이 필요합니다. Langgraph Studio는 이러한 번거로움을 덜어줍니다.


## Langgraph Studio 주요 기능

Langgraph Studio는 Langgraph 애플리케이션 개발 및 디버깅을 위한 강력한 도구입니다. 주요 기능은 다음과 같습니다.

- **시각적인 워크플로우 표현**: 정의한 워크플로우의 그래프 구성을 시각적으로 확인할 수 있습니다. 이를 통해 워크플로우의 흐름을 쉽게 이해하고 복잡한 로직을 파악할 수 있습니다.

<div style="text-align: center;">
<img src="/assets/images/Langgraph-Studio-guide/Pasted image 20250331122402.png" alt="Langgraph Studio 1" style="width: 100%; height: auto;">
</div>

- **상태 관리 및 제어**: 그래프를 만들 때 사용한 상태를 제어할 수 있는 입력 창을 제공합니다. 디버깅하려는 입력을 넣고 실행하면 워크플로우가 실행됩니다.

<div style="text-align: center;">
<img src="/assets/images/Langgraph-Studio-guide/Pasted image 20250331122611.png" alt="Langgraph Studio 1" style="width: 100%; height: auto;">
</div>

- **유연한 실행 제어**:
    - **Interrupts 옵션**: 그래프에 Interrupts 옵션을 적용하여 실행 중단을 설정할 수 있습니다.
    - **노드 선택 중단**: 특정 노드 이전이나 이후에 실행을 일시 중지하여 세밀한 디버깅이 가능합니다.

<div style="text-align: center;">
<img src="/assets/images/Langgraph-Studio-guide/Pasted image 20250331123911.png" alt="Langgraph Studio 1" style="width: 100%; height: auto;">
</div>

- **실시간 결과 확인 및 수정**: 입력값을 넣은 후, 노드 간의 결과값을 실시간으로 확인할 수 있습니다. 특정 노드의 입력값을 수정하여 다음 노드의 결과를 확인하는 등, 워크플로우 실행을 동적으로 제어할 수 있습니다.

<div style="text-align: center;">
<img src="/assets/images/Langgraph-Studio-guide/Pasted image 20250331124327.png" alt="Langgraph Studio 1" style="width: 100%; height: auto;">
</div>

- **실행 이력 관리**: 이전에 실행했던 결과를 스레드 단위로 확인할 수 있어, 과거 실행 결과를 쉽게 추적하고 비교할 수 있습니다.

<div style="text-align: center;">
<img src="/assets/images/Langgraph-Studio-guide/Pasted image 20250331124617.png" alt="Langgraph Studio 1" style="width: 100%; height: auto;">
</div>

Langgraph Studio의 가장 큰 장점은 설계한 그래프의 디버깅 기능을 시각적으로 제공한다는 점입니다. 별도의 인터페이스를 만들 필요 없이 다양한 기능을 활용하여 효율적으로 개발할 수 있습니다.

## Langgraph Studio 설치 방법
Langgraph Studio를 사용하려면 langgraph-cli 라이브러리를 설치해야 합니다. 다음 명령어를 실행하여 간단하게 설치할 수 있습니다.

```bash
pip install langgraph-cli
```

## Langgraph 실행 조건
Langgraph를 실행하려면 다음과 같은 요소들이 필요합니다.
- 컴파일된 그래프: Langgraph 워크플로우를 정의하고 컴파일한 app 변수가 필요합니다. 예를 들어:

	```python
	builder = StateGraph(QueryMakerState)

	builder.set_entry_point("DETECT_LANGUAGE")

	# 노드 추가
	builder.add_node("DETECT_LANGUAGE", detect_language_regex)
	builder.add_node(QUERY_REFINER, query_refiner_node)
	builder.add_node(GET_TABLE_INFO, get_table_info_node)
	builder.add_node(QUERY_MAKER, query_maker_node_with_db_guide)

	# 엣지 설정
	builder.add_edge("DETECT_LANGUAGE", QUERY_REFINER)
	builder.add_edge(QUERY_REFINER, GET_TABLE_INFO)
	builder.add_edge(GET_TABLE_INFO, QUERY_MAKER)
	builder.add_edge(QUERY_MAKER, END)

	app = builder.compile()
	```

- (선택 사항) `requirements.txt`: 워크플로우 실행에 필요한 파이썬 패키지 목록을 담은 파일입니다. 현재 환경을 사용하려면 파일 내용에 .을 입력하면 됩니다.
- (선택 사항) `.env`: 워크플로우에서 사용하는 API 키 등의 환경 변수를 저장하는 파일입니다.
- `langgraph.json`: Langgraph 프로젝트 설정을 정의하는 파일입니다.
	```json
	{
		"dependencies": [
			"./requirements.txt"
		],
		"graphs": {
			"agent": "./graph.py:app"
		},
		"env": ".env"
	}
	```
각 키에 대한 설명은 다음과 같습니다.
- `dependencies`: 프로젝트에 필요한 종속성 목록입니다.
- `graphs`: 실행할 그래프의 경로와 해당 그래프가 할당된 변수 이름입니다.
- `env`: 환경 변수 파일 경로입니다.

## Langgraph Studio 실행
필요한 파일들을 설정한 후, `langgraph.json` 파일이 있는 디렉토리로 이동하여 `langgraph dev` 명령어를 실행합니다. `langgraph.json` 파일이 다른 이름으로 되어 있다면 `--config` 옵션을 사용하여 지정할 수 있습니다

```bash
langgraph dev
```

또는, 설정 파일 이름이 다른 경우:

```bash
langgraph dev --config my_langgraph_config.json
```

Langsmith에 로그인되어 있지 않다면 로그인이 필요합니다. 로그인이 완료되면, 웹 브라우저에서 Langgraph Studio 인터페이스를 통해 워크플로우를 디버깅할 수 있습니다.

<div style="text-align: center;">
<img src="/assets/images/Langgraph-Studio-guide/Pasted image 20250331132858.png" alt="Langgraph Studio 1" style="width: 100%; height: auto;">
</div>


## 추가 기능: 배포
Langgraph CLI는 개발 환경뿐만 아니라 Langgraph 애플리케이션 배포를 위한 기능도 제공합니다.
- `build` 명령어: Langgraph API 서버를 위한 Docker 이미지를 빌드합니다. 이 이미지를 사용하여 다양한 클라우드 환경에 Langgraph 애플리케이션을 배포할 수 있습니다.
- `up` 명령어: 로컬 환경에서 Docker 컨테이너를 사용하여 Langgraph API 서버를 실행합니다. 로컬 개발 환경에서 배포를 테스트하는 데 유용합니다.
- `dockerfile` 명령어: Langgraph API 서버 배포를 위한 Dockerfile을 생성합니다. Docker 이미지 빌드 과정을 사용자 정의해야 하는 경우에 사용할 수 있습니다.

## 결론
Langgraph Studio와 langgraph-cli는 LLM 에이전트 개발을 위한 강력한 도구입니다. 시각적인 워크플로우 표현, 강력한 디버깅 기능, 편리한 배포 옵션을 통해 개발 생산성을 향상시키고 더 나은 LLM 애플리케이션을 만들 수 있도록 지원합니다.

## 참고 자료
- [Langgraph Studio 공식 영상](https://www.youtube.com/watch?v=o9CT5ohRHzY)
- [Langgraph cli documentation](https://langchain-ai.github.io/langgraph/cloud/reference/cli/#configuration-file)
- [LangGraph Server documentation](https://langchain-ai.github.io/langgraph/concepts/langgraph_server/)