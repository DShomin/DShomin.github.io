---
layout: post
title:  "Again Agent Protocol A2A(Agent to Agent)"
date:   2025-04-13 17:48:00 +0900
categories: LLM Review
tags: LLM Review Agent Protocol A2A
---

> 최근 Google Cloud Next '24에서 AI 에이전트 분야의 중요한 발표가 있었습니다. 바로 **Agent2Agent(A2A) 프로토콜**과 이를 구현하기 위한 **Agent Development Kit(ADK)** 의 공개입니다. 이는 Anthropic의 Model Context Protocol(MCP) 발표 이후 LLM 에이전트 상호작용 분야에서 나온 또 하나의 중요한 이정표입니다.
> 이 글에서는 A2A 프로토콜이 어떤 배경에서 등장했으며, 이 기술과 함께 공개된 ADK는 무엇인지, 그리고 이들을 활용하여 앞으로 어떤 가능성이 열릴지 살펴보고자 합니다.

## A2A(Agent-to-Agent)란 무엇인가?

A2A는 이름 그대로 **에이전트와 에이전트 간의 소통을 위한 개방형 프로토콜**입니다. 핵심 목표는 서로 다른 개발사나 프레임워크로 만들어진 AI 에이전트들이 마치 하나의 팀처럼 원활하게 정보를 교환하고 작업을 조율하여, 사용자가 요청한 복잡한 목표를 달성하도록 돕는 것입니다.

이미 스탠포드 대학의 연구([Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/abs/2304.03442))나 OpenAI의 Swarm SDK 컨셉, LangChain의 LangGraph, CrewAI 등 여러 연구와 프레임워크에서 다중 에이전트 협업(Multi-Agent System, MAS)의 가능성을 탐색해왔습니다. A2A는 이러한 흐름 속에서 '표준화된 규약'의 필요성에 대한 Google의 답변이라고 볼 수 있습니다.

<img src="/assets/images/Again-Agent-protocol-A2A/image_4.png" alt="Generative Agents: Interactive Simulacra of Human Behavior" style="width: 100%; height: auto;">

<img src="/assets/images/Again-Agent-protocol-A2A/image_5.png" alt="OpenAI Swarm" style="width: 100%; height: auto;">

## 왜 A2A 프로토콜이 필요한가?

이미 관련 기술들이 존재하는데 왜 Google은 '프로토콜'을 제안했을까요? Google은 A2A를 통해 다음과 같은 가치를 제공하고자 합니다.

1.  **상호운용성 증대**: 특정 회사나 프레임워크에 종속되지 않고, A2A 규약을 따르는 에이전트라면 누구든 서로 '대화'할 수 있습니다. 이는 마치 인터넷에서 웹사이트들이 HTTP라는 프로토콜 위에서 통신하는 것과 유사합니다.
2.  **보안 및 안정성**: 기업 환경에서의 활용을 염두에 두고 설계되어, 에이전트 간 통신 시 엔터프라이즈급 인증 및 인가를 지원하는 등 보안을 기본 원칙으로 삼습니다.
3.  **유연성 및 확장성**: 기존의 텍스트 기반 결과물 교환을 넘어 오디오, 비디오 스트리밍 등 다양한 형태(Modality)의 데이터를 지원합니다. 또한, 간단한 작업부터 인간의 개입이 필요한 장기 실행 작업까지 지원하도록 설계되었습니다.
4.  **표준 기반**: HTTP, SSE, JSON-RPC 등 이미 널리 사용되는 웹 표준을 기반으로 하여 기존 시스템과의 통합이 용이합니다.

A2A는 기존 서비스를 파괴하는 것이 아니라, 오히려 **다양한 에이전트 기술들이 서로 협력할 수 있는 '공통 언어(Common Language)'**를 제공하는 데 목적이 있습니다.

## ADK(Agent Development Kit) 공개

Google은 A2A 프로토콜 사양 발표와 함께 **ADK(Agent Development Kit)** 도 공개했습니다. ADK는 개발자들이 A2A 프로토콜을 준수하는 에이전트를 더 쉽게 구축할 수 있도록 돕는 도구, 라이브러리, 예제 코드 등을 포함합니다.

특히 ADK 예제 코드에서는 Google 자체 프레임워크뿐만 아니라, **LangGraph, CrewAI와 같은 기존의 인기 있는 에이전트 프레임워크를 사용하여 A2A 기반의 에이전트 협업을 구현하는 방법**을 보여줍니다. 이는 A2A가 특정 기술 스택에 얽매이지 않고 다양한 환경에서 적용될 수 있음을 시사하며, 개발자들이 기존 도구를 활용하면서도 A2A 생태계에 참여할 수 있도록 장려합니다.

## A2A 작동 방식

<img src="/assets/images/Again-Agent-protocol-A2A/image.png" alt="A2A Overview" style="width: 100%; height: auto;">

A2A는 크게 **클라이언트 에이전트(Client Agent)** 와 **원격 에이전트(Remote Agent)** 로 역할을 나누어 통신합니다.

1.  **클라이언트 에이전트**: 사용자의 요청을 받아 작업을 계획하고, 어떤 원격 에이전트가 해당 작업을 가장 잘 수행할 수 있는지 탐색합니다. (Capability Discovery)
2.  **원격 에이전트**: 클라이언트 에이전트로부터 작업을 위임받아 수행합니다. 필요하다면 다른 원격 에이전트와 협력하여 정보를 주고받거나(Collaboration) 추가 작업을 요청할 수도 있습니다.
3.  **작업 관리 (Task Management)**: 클라이언트와 원격 에이전트는 '작업(Task)' 객체를 중심으로 통신하며, 작업의 시작, 진행 상황 업데이트, 완료 등 명확한 수명 주기를 관리합니다. 작업의 결과물은 '아티팩트(Artifact)'라고 불립니다.
4.  **사용자 경험 협상 (UX Negotiation)**: 에이전트 간에 주고받는 메시지에는 콘텐츠 유형(텍스트, 이미지, 비디오 등)이 명시되어, 최종 사용자에게 가장 적합한 형태로 정보를 표시할 수 있도록 협상합니다.

<img src="/assets/images/Again-Agent-protocol-A2A/image_3.png" alt="A2A protocol" style="width: 100%; height: auto;">

이러한 구조는 기존 MAS 연구에서 논의되던 네트워크 방식(필요에 따라 에이전트끼리 직접 통신)과 슈퍼바이저 방식(중앙 관리 에이전트가 조율)의 특징을 혼합한 형태로 볼 수 있습니다.

<img src="/assets/images/Again-Agent-protocol-A2A/image_6.png" alt="Multi-Agent System" style="width: 100%; height: auto;">

## 강력한 파트너 생태계 (Collaborate)

Google은 A2A 프로토콜 발표와 동시에 50개 이상의 기술 및 서비스 파트너사(Atlassian, Box, Cohere, Salesforce, SAP, ServiceNow, MongoDB, LangChain, Accenture, Deloitte 등)를 확보하며 강력한 생태계 구축 의지를 보여주었습니다. 파트너사들의 면면을 보면 엔터프라이즈 소프트웨어, LLM, 데이터베이스, 결제 플랫폼, 컨설팅 등 매우 다양합니다. 이는 A2A가 특정 영역에 국한되지 않고 광범위한 분야에서 활용될 수 있음을 시사하며, 다중 에이전트 시스템의 현실화가 더욱 빨라질 수 있음을 보여줍니다.
<img src="/assets/images/Again-Agent-protocol-A2A/image_2.png" alt="A2A partners" style="width: 100%; height: auto;">

## 미래 전망

A2A 프로토콜과 ADK의 등장은 다음과 같은 미래를 기대하게 합니다.

* **손쉬운 MAS 구축**: 사용자는 특정 목적(예: 여행 계획)을 가진 클라이언트 에이전트를 정의하고, 항공권 예약, 숙소 검색, 맛집 추천 등 각 분야에 특화된 파트너사들의 원격 에이전트들을 A2A 프로토콜을 통해 연결하여 강력한 맞춤형 서비스를 구성할 수 있게 될 것입니다.
* **기업 워크플로우 혁신**: 기업 내 다양한 시스템(CRM, ERP, HR 등)에 연결된 에이전트들이 A2A를 통해 서로 소통하며 복잡한 비즈니스 프로세스(예: 신규 입사자 온보딩, 공급망 관리 최적화)를 자동화하고 효율성을 극대화할 수 있습니다.
* **새로운 서비스 모델 등장**: 특정 기능을 전문적으로 수행하는 에이전트를 개발하고 A2A를 통해 제공하는 새로운 형태의 B2B 서비스 모델이 활성화될 수 있습니다.

물론, 에이전트 간의 신뢰성, 보안, 책임 소재 등 해결해야 할 과제들도 남아있습니다. 하지만 A2A라는 표준화된 규약과 ADK라는 개발 도구는 이러한 과제들을 해결하고 에이전트 협업 시대를 앞당기는 중요한 발판이 될 것으로 기대됩니다.

## Reference

* **Google Developers Blog Post:** [Announcing the Agent2Agent Protocol (A2A)
](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/)
* **A2A Protocol Website (Examples & Overview):** <https://google.github.io/A2A/>
* **A2A GitHub Repository (Specification):** <https://github.com/google/A2A>
* **ADK agent development kit (Documentation):** <https://google.github.io/adk-docs/>
* **ADK agent development kit (GitHub):** <https://github.com/google/adk-python>
