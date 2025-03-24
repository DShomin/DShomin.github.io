---
layout: post
title:  "Deep Research와 멀티 에이전트 시스템의 최신 동향"
date:   2025-02-23 20:42:00 +0900
categories: LLM AI Research MultiAgent
tags: LLM DeepResearch MultiAgentSystem AI-Research
---

# Deep Research와 멀티 에이전트 시스템의 최신 동향

![Pasted image 20250221182116.png](/assets/images/DeepResearch_with_MAS/Pasted_image_20250221182116.png)

![Pasted image 20250221133141.png](/assets/images/DeepResearch_with_MAS/Pasted_image_20250221133141.png)

![Pasted image 20250221133218.png](/assets/images/DeepResearch_with_MAS/Pasted_image_20250221133218.png)

![Pasted image 20250221133159.png](/assets/images/DeepResearch_with_MAS/Pasted_image_20250221133159.png)

## Intro

최근 AI 연구 분야에서 가장 주목받고 있는 영역 중 하나는 'Deep Research' LLM 서비스와 멀티 에이전트 시스템입니다. 이 글에서는 ChatGPT, Perplexity, Gemini, Grok 등 우후죽순으로 발표되고 있는 Deep Research LLM 서비스들의 작동 원리와 멀티 에이전트 시스템과의 관계를 심층적으로 탐구해보고자 합니다.

> **참고**: 본 글에서 공유하는 내용 중 일부는 Deepseek를 제외하고는 공개된 자료가 많지 않아 추정에 기반한 분석임을 미리 밝힙니다.

## DeepResearch 방식 해체 분석

Deep Research LLM 서비스들은 공통적으로 **계획 → 검색 → 답변생성**이라는 3단계 워크플로우를 따릅니다. 여기서 서비스별로 가장 큰 차이점은 첫 번째 '계획' 단계에서 나타납니다. (일부 서비스에서는 이를 'Thinking'이라고 표현하기도 하지만, 이 글에서는 보다 포괄적인 의미의 '계획 단계'라는 용어를 사용하겠습니다.)

### 1. 계획 단계

![Deepseek의 Thinking 수행](/assets/images/DeepResearch_with_MAS/image.png)
*Deepseek의 Thinking 프로세스*

최근 발표된 Deepseek-R1 논문에 따르면, 이 모델은 `<THINK>` 토큰을 활용하여 사용자 질문에 대한 사고 과정을 우선적으로 수행한 후 이를 바탕으로 답변을 생성합니다. 이는 Transformer 모델의 Auto-regressive 특성을 활용한 방식으로, 논리적 사고 과정을 먼저 생성함으로써 최종 답변의 품질을 향상시키는 전략입니다.

![Auto-regressive](/assets/images/DeepResearch_with_MAS/Pasted_image_20250222232454.png)
*Auto-regressive 방식의 동작 원리*

다른 Deep Research 서비스들도 유사한 방식을 채택했을 가능성이 높지만, 공식 자료가 부족하여 정확한 메커니즘은 확인하기 어렵습니다. 가능성이 높은 대안적 접근법으로는 "사용자 질문을 읽고 연구를 위한 워크플로우를 설계하세요"와 같은 연구 지향적 프롬프트를 통해 계획 단계를 수행하는 방식이 있을 것으로 추정됩니다.

### 2. 검색 단계

![검색 프로세스](/assets/images/DeepResearch_with_MAS/Pasted_image_20250221191509.png)
*검색 단계의 일반적 프로세스*

계획 단계에서 식별된 필요 정보를 수집하기 위해, 시스템은 관련 키워드를 추출하여 검색 API를 통해 정보를 수집합니다. 이 검색 단계는 대부분의 서비스에서 유사한 형태로 구현되었을 것으로 예상됩니다. 이 부분은 멀티 에이전트 시스템과 밀접한 관련이 있으며, 뒤에서 더 자세히 다루도록 하겠습니다.

### 3. 답변 생성 단계

![답변 생성 프로세스](/assets/images/DeepResearch_with_MAS/Pasted_image_20250221191533.png)
*답변 생성 단계의 일반적 프로세스*

검색 단계에서 수집된 정보(컨텍스트)를 바탕으로, 사용자가 요청한 구조와 포맷에 맞춰 최종 답변을 생성합니다. 이 과정에서는 검색 단계에서 활용한 참조 자료도 함께 제시하여 답변의 신뢰성을 높입니다.

### 4. 사용자 개입 (Human In The Loop)

![OpenAI의 DeepResearch](/assets/images/DeepResearch_with_MAS/Pasted_image_20250221232900.png)
*OpenAI의 DeepResearch 사용자 개입 인터페이스*

보다 전문적인 용어로는 'Human In The Loop(HITL)'라고 불리는 이 단계에서는, 시스템이 사용자에게 추가 질문을 던져 더 정확하고 맞춤화된 답변을 생성할 수 있도록 합니다. 현재 이 기능은 OpenAI와 Google의 서비스에서만 제공되고 있습니다.

두 서비스의 HITL 접근법에는 중요한 차이가 있습니다:
- **Gemini**: 사용자 질문 직후 계획을 생성하고, 사용자가 이를 직접 수정할 수 있는 인터페이스 제공
- **ChatGPT**: 사용자 질문에 대한 추가 질문을 통해 계획을 정교화하지만, 사용자가 계획 자체를 직접 수정할 수는 없음

![Gemini HITL 인터페이스](/assets/images/DeepResearch_with_MAS/image%201.png)
*Gemini의 사용자 개입 인터페이스*

![ChatGPT HITL 인터페이스](/assets/images/DeepResearch_with_MAS/image%202.png)
*ChatGPT의 사용자 개입 인터페이스*

### 각 서비스별 비용 비교

| **서비스** | **요금제 이름** | **월 요금** | **사용 제한** |
| --- | --- | --- | --- |
| GPT Pro | ChatGPT Pro | $200 USD | 월 100회 사용 가능 |
| 퍼플렉시티 | 정보 부족 | $20 USD | 횟수 제한 없음 |
| 제미나이 | Gemini Advanced | ₩29,000 | 제한 정보 없음 (첫 달 무료) |
| Grok3 | X Premium+ | $30 USD | 제한 정보 없음 |

## 멀티 에이전트 시스템(Multi-Agent System)

작년부터 AI 분야에서 각광받고 있는 '에이전트(Agent)' 개념을 살펴보겠습니다. 앞서 소개한 Deep Research LLM 서비스들도 넓은 의미에서 에이전트 시스템의 한 유형으로 볼 수 있으며, 특히 검색 기능은 에이전트의 대표적인 구현 사례입니다.

### Re-Act(Reasoning-Acting)

![Re-Act 개념도](/assets/images/DeepResearch_with_MAS/Pasted_image_20250221175807.png)
*Re-Act 프레임워크 개념도*

Re-Act는 LLM이 시스템의 함수나 API를 직접 활용할 수 있게 함으로써, LLM의 가장 큰 문제점 중 하나였던 할루시네이션(환각) 문제를 효과적으로 해결하는 접근법입니다.

### CoT(Chain of Thought) & ToT(Tree of Thought)

![CoT와 ToT 비교](/assets/images/DeepResearch_with_MAS/Pasted_image_20250221175603.png)
*Chain of Thought와 Tree of Thought 비교*

Deep Research 서비스의 계획 단계와 밀접하게 연관된 에이전트 방법론으로 CoT(Chain of Thought)와 ToT(Tree of Thought)가 있습니다.

CoT는 복잡한 사용자 질문을 여러 하위 질문으로 분해하여 각각에 대한 답변을 종합하는 방식인 반면, ToT는 질문에 대한 여러 가능한 접근법을 동시에 탐색하는 방식입니다. 다이어그램에서는 여러 경로를 동시에 탐색하는 것으로 묘사되어 있지만, 실제 Deep Research 서비스들은 계산 효율성을 위해 가장 유망한 단일 경로만을 선택해 진행할 것으로 추정됩니다.

![사고 과정 시각화](/assets/images/DeepResearch_with_MAS/Pasted_image_20250216193838.png)
*사고 과정의 시각화*

### 최신 멀티 에이전트 시스템 사례

#### 1. STORM(Synthesis of Topic Outlines through Retrieval and Multi-perspective Question Asking)

![STORM 아키텍처](/assets/images/DeepResearch_with_MAS/Pasted_image_20250222003202.png)
*STORM 시스템 아키텍처*

스탠포드 대학에서 개발한 STORM은 주목할 만한 멀티 에이전트 시스템입니다. 이 시스템의 핵심 원리는 다음과 같습니다:

1. 사용자 질문에 적합한 다양한 '분석가' 페르소나를 시스템 내부에서 자동 생성
2. 생성된 페르소나와 각 분야의 '전문가' 에이전트 간의 인터뷰 진행
3. 인터뷰 결과를 바탕으로 필요한 정보를 검색하고 보충
4. 최종적으로 보고서의 각 섹션별로 체계적인 답변 생성

#### 2. Agent Laboratory

![Agent Laboratory 개념도](/assets/images/DeepResearch_with_MAS/Pasted_image_20250221160213.png)
*AMD의 Agent Laboratory 개념도*

AMD에서 최근 발표한 'Agent Laboratory'는 STORM과 유사하게 페르소나 간의 소통을 활용하지만, 특별히 AI 연구실 환경에 최적화된 에이전트들을 미리 정의했다는 점에서 차이가 있습니다.

![Agent Laboratory 워크플로우](/assets/images/DeepResearch_with_MAS/image%203.png)
*Agent Laboratory의 워크플로우*

이 시스템은 단순한 텍스트 답변 생성에 그치지 않고, Python 스크립트의 작성・수정・실행까지 담당하며, 생성된 모델에 대한 평가도 자동으로 수행합니다. 최종적으로는 연구 결과를 논문 형식으로 정리하고, '리뷰어' 에이전트들의 피드백을 통해 품질을 개선하는 과정까지 포함하고 있습니다.

![Agent Laboratory 성능 결과](/assets/images/DeepResearch_with_MAS/image%204.png)
*Agent Laboratory의 우수한 성능 결과*

![결과물 예시](/assets/images/DeepResearch_with_MAS/image%205.png)
*Agent Laboratory가 생성한 결과물 예시*

#### 3. Google Co-scientist

![Google Co-scientist](/assets/images/DeepResearch_with_MAS/Pasted_image_20250221160605.png)
*Google Co-scientist 시스템*

Google의 'Co-scientist'는 Agent Laboratory와 유사하지만 특별히 과학 연구 분야에 특화된 멀티 에이전트 시스템입니다.

![Co-scientist 성과](/assets/images/DeepResearch_with_MAS/Pasted_image_20250221160610.png)
*Co-scientist의 주요 성과*

특히 주목할 만한 점은, 기존에 수십 년이 걸렸던 특정 연구를 단 몇 일 만에 해결했다는 사례가 보고되었다는 것입니다.

<video width="640" height="480" controls>
  <source src="/assets/images/DeepResearch_with_MAS/AI_Co-Scientist_Hero.mp4" type="video/mp4">
  AI Co-Scientist Hero
</video>


## 결론 및 전망

Deep Research 서비스와 다양한 멀티 에이전트 시스템을 비교 분석한 결과, 다음과 같은 인사이트를 얻을 수 있습니다:

1. **접근법의 차이**: Deep Research 서비스는 STORM과 유사한 접근법을 취하고 있으나, 서비스 확장성을 위해 과도한 LLM 호출이 필요한 인터뷰 과정은 생략하고 가장 유망한 계획만을 수행하는 방식을 채택했습니다. 이는 서비스 효율성을 높이지만, 단일 관점에만 의존하게 되어 정보의 다양성 측면에서는 제한될 수 있습니다.

2. **특화 vs 범용**: Agent Laboratory와 Google Co-scientist가 특정 도메인(AI 연구, 과학 연구)에 최적화된 시스템인 반면, Deep Research 서비스와 STORM은 보다 범용적인 문제 해결을 목표로 합니다.

3. **미래 전망**: 최근 에이전트 기술이 각광받는 이유는 기업과 개인이 자신의 도메인에 특화된 시스템을 구축하거나, 업무 효율성을 극대화하는 데 이러한 기술이 큰 잠재력을 보여주고 있기 때문입니다.

![미래 전망](/assets/images/DeepResearch_with_MAS/Pasted_image_20250221155144.png)
*멀티 에이전트 시스템 in Langgraph*

향후 멀티 에이전트 시스템은 더욱 전문화되고 개인화될 것으로 예상됩니다. 특히 특정 업무 영역에 최적화된 에이전트들이 서로 협업하는 생태계가 형성되면서, 인간-AI 협업의 새로운 패러다임이 형성될 것으로 전망됩니다. Deep Research 서비스들도 이러한 흐름에 맞춰 더욱 정교한 계획 단계와 사용자 개입 메커니즘을 발전시켜 나갈 것으로 기대됩니다.