## 개요
3학년 2학기 로봇 프로그래밍(ROS) 도로주행시험장 자율주행 프로젝트입니다.

## 비전
![image](https://user-images.githubusercontent.com/56144682/148673097-02f713e1-4c48-4356-9e02-5e1d9a269d66.png)  
우리나라는 2011년부터 지금까지 꾸준히 차 보급률이 높아지면서 2020년에는 2,437만 대의 차를 보유하고 있다.   이처럼 차를 보유하고 있는 사람들이 많아지면서 도로교통사고에 대한 피해도 꾸준하게 발생하고 있다.  
   
교통 사고분석시스템에 따르면 2020년 교통사고는 209,654건으로 대형사고 사망자는 전년 대비 11.4%나 증가할 만큼 사고가 자주 일어나고 있다. 또한, 이를 처리하기 위해 사용되는 도로교통 비용이 약 25조 9,000억에 달할 만큼 어마어마한 지출이 발생한다. 이러한 사고는 운전자의 안전운전 불이행이 전체 교통사고의 61.3%로 절반 이상을 차지하고 있을 만큼 운전자의 운전 습관이 사고로 직결되는 경우가 많다.  
많은 전문가가 자율주행이 필요한 이유로 안전성을 꼽는데 자율주행이 이루어지면 교통사고 발생 원인의 98%인 운전자의 변수 요인을 제거하여 운전자는 주행 상황에서 자유롭고 더욱 안전하게 주행할 수 있다. 또한, 교통사고를 줄일 수 있다는 것 외에도 운전하는 시간을 다른 생산적인 일에 활용할 수 있고 이동시간을 최적화할 수 있다.  
최근에는 IT 기기를 주력으로 삼는 회사인 애플사에서 2025년에는 페달과 핸들이 없는 완전 자율주행 전기차를 출시하겠다는 발표와 더불어 우리나라에서도 2025년엔 자동차가 스스로 모든 기능을 제어하는 고도 자율주행(4단계)을 상용화할 것이라는 현대사의 발표와 더불어 자율주행 자동차 상용화 지원을 위한 범부처 실행계획을 수립하여 관련 사업을 추진하고 있을 만큼 국내외 모두 자율주행 자동차에 관한 관심이 높아지는 것을 알 수 있다.  
   
이러한 산업이 발전하면서 관련한 로봇 소프트웨어 산업이 폭발적으로 성장하고 있음에 따라 우리도 로봇 프로그래밍을 통해 로봇의 구동을 이해하고 실제 도로와 비슷한 환경에 맞춰 테스트하고 이해하는 것이 목적이다. 이전에 배웠던 디자인 패턴 활용하여 객체 지향적으로 설계하며 로봇의 자율주행과 도로 주행시험장에서 발생하는 다양한 문제들을 인식하고 해결하는 능력을 갖춘 로봇(터틀봇) 프로그램을 python과 gazebo 도구를 활용하여 개발한다.  

## 요구사항 명세서
1) 두 차선 중 지정한 차선(1, 2번)에 로봇을 위치시켜야 한다. 앞에 위치한 차단바가 올라가면 출발한다. 터틀봇의 최대 속도는 1m/sec을 초과해서는 안 된다.
2) 정지선 앞에서 3초 간 정지해야 한 후 출발한다.
3) 해당 사항 없음.
4) 두 개의 굴절코스 중 하나를 선택하여 통과한다. 
5) 정지선 앞에 정지한 후 전방 신호등의 녹색등이 켜지면 출발하여 직진한다.
6) 두 개의 곡선코스 중 하나를 선택하여 통과한다. 
7) 정지선 앞에 정지한 후 전방 신호등의 녹색등이 켜지면 출발하여 직진한다.
8) 두 개의 방향전환코스 중 하나를 선택하여 통과한다. (실제 지도 제공 시 방향전환코스는 
   두 개만 주어질 예정임.)
9) 정지선 앞에 정지한 후 전방 신호등의 좌회전 신호등이 켜지면 출발하여 죄회전한다.
10) 정지 신호등을 인식한 후, 정지선 앞에 정지한다. 3초 후 출발한다.
11) 3개의 장애물을 충돌하지 않고 통과해야 한다.
12) 평행주차 코스에 도달하면 지정된 공간에 들어가서 3초 간 대기 후 다시 도로에 진입하여 직진한다.
13) 정지선 앞에 3초 간 정지 후, 우회전한다.
14) (노란 색) 종료 정지선 앞에 정지한다. 

## Turtle Bot Node 통신 구조
![image](https://user-images.githubusercontent.com/56144682/148673324-784deaa3-c349-4cdc-9807-c371ed5ecc4f.png) 
gazebo의 ‘camera’ 노드와 ‘LIDAR’ 노드와 깊이 카메라, 터틀봇의 기본 이동 요소를 담당하는 노드와 같이 기본적인 하드웨어 모듈 노드로부터 필요한 정보를 직접 생성한 토픽 노드를 통해 추출하였다. 해당 노드들로부터 수집한 정보는 최종적으로 ‘drive’ 노드로 전송되어 터틀봇을 최종 구동시킨다.  

## 분석
### Detect Blocking bar
**Usecase Diagram**  
![image](https://user-images.githubusercontent.com/56144682/148673372-58bef1f5-0442-4faf-9b03-1197ef1bb529.png)  

**Sequence Diagram**  
![image](https://user-images.githubusercontent.com/56144682/148673345-dd93bd5a-04cf-42d2-bc22-ef493648301e.png)  
 
**Domain Model**  
![image](https://user-images.githubusercontent.com/56144682/148673393-c052f1a0-6cf1-4b69-8f11-f071a8cf3e68.png)  

**구현**  
![image](https://user-images.githubusercontent.com/56144682/148673380-7e4dfd67-264a-4f30-ba94-c70396c38c5c.png)  
---  
### Detect Stop line
**Usecase Diagram**  
![image](https://user-images.githubusercontent.com/56144682/149340262-1f4e6fa2-f87b-4ff5-9c2b-31295fecd3cd.png)

**Sequence Diagram**  
![image](https://user-images.githubusercontent.com/56144682/149340305-53cd84ad-1891-4169-b6ea-61ad6efad21f.png)  
 
**Domain Model**  
![image](https://user-images.githubusercontent.com/56144682/149340312-cf889d0f-235e-4323-9706-4c5f537c4410.png)  

**구현**  
![image](https://user-images.githubusercontent.com/56144682/149340282-9dd2b68c-6af0-46ce-b545-72789599187f.png)  
---  
### Detect Obstacle
**Usecase Diagram**  
![image](https://user-images.githubusercontent.com/56144682/149340421-7570d9e7-bc13-4db6-8ff2-59eadb6e4048.png)  

**Sequence Diagram**  
![image](https://user-images.githubusercontent.com/56144682/149340458-fa54c096-e407-499c-aa1c-ded1ed40f0cb.png)  
 
**Domain Model**  
![image](https://user-images.githubusercontent.com/56144682/149340440-66576dc3-45a2-41c8-9246-88b065aa95ce.png)  
**구현**  
![image](https://user-images.githubusercontent.com/56144682/149340641-cd6f638e-ad0d-4209-815c-14b3e6f599de.png) 
---  
### Detect Stop Sign
**Usecase Diagram**  
![image](https://user-images.githubusercontent.com/56144682/149340759-3924964f-d2ef-45c9-b05f-aecc15d9e8aa.png)  

**Sequence Diagram**  
![image](https://user-images.githubusercontent.com/56144682/149340886-913f0ce7-b2ad-445e-ac7b-4867e86fc876.png)  
 
**Domain Model**  
![image](https://user-images.githubusercontent.com/56144682/149340965-ef17a39f-f518-42ae-9313-ee1e0e549a85.png)  
**구현**  
![image](https://user-images.githubusercontent.com/56144682/149340873-22ccc18d-eb58-4d07-a1a7-ba822e992202.png)
---
### Detect Stop Sign
**Usecase Diagram**  
![image](https://user-images.githubusercontent.com/56144682/149340421-7570d9e7-bc13-4db6-8ff2-59eadb6e4048.png)  

**Sequence Diagram**  
![image](https://user-images.githubusercontent.com/56144682/149340458-fa54c096-e407-499c-aa1c-ded1ed40f0cb.png)  
 
**Domain Model**  
![image](https://user-images.githubusercontent.com/56144682/149340440-66576dc3-45a2-41c8-9246-88b065aa95ce.png)  
**구현**  
![image](https://user-images.githubusercontent.com/56144682/149340641-cd6f638e-ad0d-4209-815c-14b3e6f599de.png) 
---  
### Detect Left/Right Line
**Usecase Diagram**  
![image](https://user-images.githubusercontent.com/56144682/149341124-098c1c65-1b23-4d5a-ab61-adf26fa72919.png)  
**Sequence Diagram**  
![image](https://user-images.githubusercontent.com/56144682/149341143-e0262d45-4f9f-4519-bacb-1d407077a8fb.png)  
**Domain Model**  
![image](https://user-images.githubusercontent.com/56144682/149341110-2d990d42-e8c7-47e5-bc22-4b72e4526070.png)  
**구현**  
![image](https://user-images.githubusercontent.com/56144682/149341165-4173ec81-7b9a-4099-9d3f-b705f30ec28f.png)  
---
### Left/Right Line Tracer
**Usecase Diagram**  
![image](https://user-images.githubusercontent.com/56144682/149341488-02e48a58-45f5-4bad-bf95-73f1ae4faad1.png)  
![image](https://user-images.githubusercontent.com/56144682/149341531-140641c1-8b72-4503-92c6-7f32d3aa6299.png)  

**Sequence Diagram**  
![image](https://user-images.githubusercontent.com/56144682/149341632-9bdae065-6070-4975-b88f-f71bcc8a1635.png)
**Domain Model**  
![image](https://user-images.githubusercontent.com/56144682/149341567-085672ad-0687-40f0-ab55-ba985cf2a061.png)  
**구현**  
![image](https://user-images.githubusercontent.com/56144682/149341618-2b3b0cf3-236a-4a19-b579-c9d13506ef1d.png) 

# 주행영상

#### Track 1
![1차선_주행영상](https://youtu.be/bdb_rHeUrW8)

#### Track 2
![2차선_주행영상](https://youtu.be/48nuG1fZVoE)
