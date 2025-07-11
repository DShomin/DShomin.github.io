---
layout: post
title:  "Multi-Agent System 설계: 직렬 vs 병렬 구조의 선택 기준"
date:   2025-07-11 18:50:00 +0900
categories: LLM AI Research MultiAgent
tags: MultiAgentSystem LLM AI-Agent Cognition Anthropic LangChain Architecture
---

# Multi-Agent System 설계: 직렬 vs 병렬 구조의 선택 기준

## 들어가며

2025년 AI Agent 생태계에서 가장 흥미로운 논쟁 중 하나가 전개되었습니다. 6월 12일 Cognition AI가 "Don't Build Multi-Agents"라는 도발적인 글을 발표했고, 바로 다음 날 Anthropic이 "How we built our multi-agent research system"으로 대응하며 Multi-Agent System(MAS) 설계에 대한 근본적인 관점 차이가 드러났습니다.

이러한 상반된 입장은 단순한 기술적 견해 차이를 넘어서, AI Agent 시스템의 미래 아키텍처에 대한 철학적 차이를 보여줍니다. 본 글에서는 이 두 접근 방식을 분석하고, MAS 구축 시 고려해야 할 핵심 원칙들을 살펴보겠습니다.

## Cognition의 관점: "Don't Build Multi-Agents"

### 핵심 논제: Context Isolation의 문제

Cognition의 핵심 주장은 병렬로 동작하는 sub-agent들이 context isolation으로 인해 본질적으로 취약하다는 것입니다. 그들이 제시한 "Flappy Bird" 예시가 이를 잘 보여줍니다: 한 sub-agent는 Super Mario 배경을 만들고, 다른 agent는 게임이 아닌 새 캐릭터를 만드는 상황이 발생할 수 있습니다. 이는 각 agent가 다른 agent의 행동이나 암묵적인 설계 결정에 대한 공유 맥락이 없기 때문입니다.

![image](https://cdn.sanity.io/images/2mc9cv2v/production/721e44474051c62156e15b5ffb1a249c996f0607-1404x1228.png)

### Context Engineering의 중요성

Cognition은 "Context Engineering"이라는 개념을 도입했습니다. 이는 단순한 프롬프트 엔지니어링을 넘어서, 동적 시스템에서 자동으로 적절한 맥락을 제공하는 것을 의미합니다. 그들의 두 가지 핵심 원칙은 다음과 같습니다:

1. **완전한 맥락 공유**: Agent들은 단순한 메시지가 아닌 완전한 agent trace를 포함한 전체 맥락을 공유해야 함
2. **직렬 구조 선호**: 신뢰성을 위해 단일 스레드, 선형적 agent 구조를 선호

![image](https://cdn.sanity.io/images/2mc9cv2v/production/836a7407ddf3dfacc0715c0502b4f3ffc7388829-1406x1230.png)

### 코딩 작업에서의 한계

코딩 작업은 대부분 연구 작업보다 진정으로 병렬화할 수 있는 작업이 적으며, LLM agent들은 아직 실시간으로 다른 agent들과 효과적으로 조율하고 위임하는 데 능숙하지 않습니다. 이는 Devin과 같은 코딩 agent가 multi-agent 접근 방식을 피하는 이유를 설명합니다.

## Anthropic의 관점: Multi-Agent Research System

### 병렬 처리의 성능 우위

Anthropic의 내부 평가에서 Claude Opus 4를 주도 agent로, Claude Sonnet 4를 sub-agent로 사용하는 multi-agent 시스템이 단일 Claude Opus 4 agent보다 90.2% 더 우수한 성능을 보였습니다. 특히 S&P 500 IT 기업들의 이사회 구성원을 모두 찾는 작업에서, multi-agent 시스템은 작업을 sub-agent들에게 분해하여 정확한 답을 찾았지만, 단일 agent 시스템은 느리고 순차적인 검색으로 실패했습니다.

### Orchestrator-Worker 패턴

Anthropic의 Research 시스템은 주도 agent가 전체 프로세스를 조율하고 병렬로 동작하는 전문 sub-agent들에게 작업을 위임하는 orchestrator-worker 패턴을 사용합니다. 이 구조의 핵심은:

1. **동적 적응성**: 정적 파이프라인과 달리 발견 사항에 따라 지속적으로 접근 방식을 업데이트
2. **맥락 압축**: 각 sub-agent가 자체 맥락 창에서 병렬로 작업하여 정보를 압축
3. **관심사 분리**: 각 sub-agent가 고유한 도구, 프롬프트, 탐색 경로를 가짐
![image](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F1198befc0b33726c45692ac40f764022f4de1bf2-4584x2579.png&w=3840&q=75)

### 토큰 사용량과 경제성

Multi-agent 시스템의 성능 향상은 주로 문제 해결을 위해 충분한 토큰을 사용할 수 있기 때문입니다. 토큰 사용량만으로도 성능 분산의 80%를 설명할 수 있습니다. 하지만 이는 경제적 비용을 수반합니다: 일반적으로 agent는 채팅 상호작용보다 약 4배 많은 토큰을 사용하고, multi-agent 시스템은 채팅보다 약 15배 많은 토큰을 사용합니다.

## LangChain의 종합: "How and When to Build Multi-Agent Systems"

### Read vs Write 작업의 구분

LangChain의 Harrison Chase는 두 접근 방식을 종합하며 핵심 통찰을 제시했습니다: "읽기" 작업을 위한 multi-agent 시스템이 "쓰기" 작업보다 관리하기 쉽다는 것입니다.

**읽기 작업의 특징:**
- 본질적으로 더 병렬화 가능
- 충돌하는 읽기 작업이 상대적으로 덜 해로움
- 연구, 정보 수집, 분석 등에 적합

**쓰기 작업의 특징:**
- 병렬화 시 맥락 전달과 출력 병합의 이중 도전
- 충돌하는 쓰기 작업이 호환되지 않는 출력 생성
- 코딩, 콘텐츠 작성 등에서 복잡성 증가

### 실용적 가이드라인

Multi-agent 시스템은 다음 조건에서 탁월합니다:
- 여러 독립적인 방향을 동시에 추구하는 breadth-first 쿼리
- 단일 agent의 한계를 초과하는 작업
- 높은 병렬화가 필요한 가치 있는 작업
- 단일 맥락 창을 초과하는 정보를 다루는 작업
- 수많은 복잡한 도구와의 인터페이스가 필요한 작업

## 설계 원칙과 실무 지침

### Context Engineering 구현

1. **명확한 작업 분해**: 각 sub-agent는 목적, 출력 형식, 도구 사용 지침, 명확한 작업 경계가 필요합니다.

2. **복잡성에 따른 리소스 조정**: 단순한 사실 확인은 1개 agent로 3-10회 도구 호출, 복잡한 연구는 10개 이상의 sub-agent가 명확히 분리된 책임을 가지도록 설계

3. **도구 설계의 중요성**: Agent-도구 인터페이스는 인간-컴퓨터 인터페이스만큼 중요하며, 각 도구는 고유한 목적과 명확한 설명이 필요합니다.

### 평가와 디버깅

1. **소규모로 시작**: 초기 개발에서는 20개 정도의 테스트 케이스로도 변화의 영향을 명확히 파악할 수 있습니다.

2. **LLM-as-Judge 활용**: 연구 결과는 프로그래밍 방식으로 평가하기 어려우므로 LLM을 판사로 사용하는 것이 자연스럽습니다.

3. **인간 평가의 필수성**: 자동화가 놓치는 edge case, 시스템 실패, 미묘한 소스 선택 편향 등을 발견하는 데 인간 테스터가 필수적입니다.

## 결론: 상황에 맞는 아키텍처 선택

이 논쟁을 통해 얻을 수 있는 핵심 교훈은 "one-size-fits-all" 솔루션은 없다는 것입니다. 대신 해결하고자 하는 문제에 따라 여러 옵션을 탐색하고 최적의 것을 선택해야 합니다.

**Multi-Agent 시스템이 적합한 경우:**
- 광범위한 연구와 정보 수집 작업
- 병렬 처리가 가능한 독립적 하위 작업들
- 단일 맥락 창을 초과하는 복잡한 작업
- 높은 가치로 인해 토큰 비용을 정당화할 수 있는 작업

**Single-Agent 시스템이 적합한 경우:**
- 일관성과 논리적 연결성이 중요한 작업
- 강한 상호 의존성을 가진 작업들
- 실시간 맥락 공유가 필수적인 작업
- 비용 효율성이 중요한 일상적 작업

결론적으로, 이 논쟁의 진정한 가치는 Cognition의 신중함과 Anthropic의 야심을 종합하는 것입니다. 단일 모델 맥락의 근본적 한계를 극복하기 위해 병렬 multi-agent 아키텍처를 수용하되, 고유한 복잡성을 관리하는 데 필요한 엄격한 엔지니어링 원칙을 적용해야 합니다.

앞으로의 방향은 명확합니다. 능동적이고 환경적인 제어 루프를 중심으로 설계된 새로운 클래스의 agent 시스템이 필요하며, 이는 정밀한 위임을 하는 견고한 오케스트레이션, 준선형적으로 확장되는 고급 메모리 관리, 그리고 agent의 마음의 결정론적 확장 역할을 하는 상태 유지 도구들을 특징으로 해야 합니다.

## 참고 자료

### 주요 논문 및 블로그 포스트

1. **Cognition AI**: ["Don't Build Multi-Agents"](https://cognition.ai/blog/dont-build-multi-agents#applying-the-principles) - 2025년 6월 12일
2. **Anthropic**: ["How we built our multi-agent research system"](https://www.anthropic.com/engineering/built-multi-agent-research-system) - 2025년 6월 13일  
3. **LangChain**: ["How and When to Build Multi-Agent Systems"](https://blog.langchain.dev/how-and-when-to-build-multi-agent-systems/) - Harrison Chase의 분석

### 관련 기술 자료

- **Context Engineering**: Multi-Agent 시스템에서 맥락 공유의 중요성
- **Orchestrator-Worker Pattern**: 병렬 처리를 위한 아키텍처 패턴
- **Token Economics**: Multi-Agent 시스템의 비용 효율성 분석