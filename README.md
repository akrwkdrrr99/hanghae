# hanghae
# MovieW 📺

본인의 추천 영화 리스트를 뽐내보세요 ! 😉
<br>추천된 영화들을 모아 인기순위를 보여드려요
<br>다른 사람들이 추천한 영화도 살펴보며 자신만의 인생영화를 겟 하세요 !
<br>추천 하고 추천 받는 영화리뷰 사이트 Moview 👍

<br>

## 1. 제작 기간 & 팀원 소개
- 2022년 3월 7일 ~ 2022년 3월 10일
- 4인 1조 팀 프로젝트
  + 박형기 : 게시글 관련 페이지
  + 김원희 : 마이페이지
  + 유학선 : Main_index 페이지, 페이지 구조 설계
  + 김승균 : 로그인 페이지 및 화면들 기본 Layout.html 제작

<br>

## 2. 사용 기술
`Back-end`
- Python 3.8
- Flask 2.0.3
- MongoDB 5.0.6
- JWT 인증
- BS4 , Requests [크롤링]

`Front-end`
- JQuery 3.5.1
- Bootstrap 5.0.2
- Jinja2 템플릿 언어

`deploy`
- AWS EC2 (Ubuntu 18.04 LTS)

<br>

## 3. 실행화면

<img src="https://media-sparta.s3.amazonaws.com/media/tempvideos/20220310/%EC%8D%B8%EB%84%A4%EC%9D%BC_42.png">

자세한 영상 : <b>https://youtu.be/_1Q7TSXGmMw</b>

<br>

## 4. 핵심기능

+ **로그인, 회원가입, 마이페이지**   
  : JWT를 이용하여 로그인과 회원가입을 기능 구현
  <br>: Jinja2를 사용하여 layout.html을 유지한 채 나머지 페이지들을 작업하여 효율성 증대
  <br>: 아이디와 닉네임의 중복확인 기능 구현
  <br>: 마이페이지에서 회원정보 수정 기능 구현
  <br>: 마이페이지에서 내가 작성한 게시글 모아보기 기능 구현
  <br>: 아이디 찾기 & 비밀번호 찾기 기능 구현
  <br>: 회원탈퇴 기능 구현

+ **Main_index 페이지**   
  : 영화 리스트업 기능 구현
  <br>: 리스트업 내 소트 기능 구현
  <br>: 리모트 버튼 구현

+ **게시글 관련 페이지**   
  : 게시판 기능 구현
  <br>: 페이지네이션 기능 구현
  <br>: 목록 버튼 & 이동 버튼 & 게시글 등록 기능 구현
  <br>: 검색 기능 구현

<br>

## 5. 우리 팀이 해결한 문제
1. 게시글 페이지 네이션
  - mongoDB 기본 함수 중에 skip() 및 limit() 사용해서 페이지를 구현
  (참고 자료 : https://www.codementor.io/@arpitbhayani/fast-and-efficient-pagination-in-mongodb-9095flbqr)
2. ID , 비밀번호 찾기 
  - 다른 사이트들의 ID,비밀번호 찾기를 직접 해보면서 우리가 어떻게 구현할지 고민

<br>

## 6. 개인 회고
: <b>추후 추가 예정 !</b>
