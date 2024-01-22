# EZ2PATTERN SERVER
![img1](https://github.com/Wintiger0222/ez2pattern_server/assets/24960466/9ef367e9-b157-4e5e-8f59-c422776095c4)
EZ2ON REBOOT : R / DJMAX RESPECT V의 게임내의 패턴을 확인 할 수 있는 [EZ2PATTERN](https://ez2pattern.kro.kr/)의 프로젝트
## 개요
* 개인 프로젝트
* 프로젝트 제작 기간 : 2023-11-23 ~ 작성일 기준 2024-01-22
* 참여 인원 3명
    * 프로젝트 제작: 1명
    * 데이터 제공: 2명

### 프로젝트 설명 
 * 게임 내에서 플레이 할 수 있는 곡의 여러 패턴을 확인할 수 있다.
 * 조건에 따라 게임 내 곡의 리스트를 확인 할 수 있다.
 * 패턴에 랜덤 옵션을 적용했을때 예상값을 확인 할 수 있다.

### 기획 의도
스팀에서 서비스 하는 EZ2ON REBOOT : R이라는 리듬 게임에서 패턴을 볼 수 있는 서비스가 있으면 좋겠다고 생각했습니다.

[sdvx.in](https://sdvx.in/) 과 같은 타게임을 위한 서비스가 존재하기 때문에 이를 모방하여 EZ2ON REBOOT : R에 도 이런 사이트를 만들고자 했습니다.

## 사용 스택
### FrontEnd
* HTML
* CSS
* JS

### BackEnd
* Nginx
* Django
* SQLite

### Etc
* Oracle Cloud
* VSCode & Github
## 프로젝트 구조
![image](https://github.com/Wintiger0222/ez2pattern_server/assets/24960466/4c24d040-5f1a-445b-914d-0a80b6965ca4)

기존적인 Django의 구조를 따라갑니다.

게임별로 모듈을 분리하여서, 다른 게임에 대한 서비스의 추가가 용이합니다.

이후 서비스를 진행하면서 DJMAX RESPECT : V(djmax)라는 서비스도 추가하였으나, 주로 ez2on 위주로 설명을 하겠습니다.

## 기능 설명
![image](https://github.com/Wintiger0222/ez2pattern_server/assets/24960466/75b8d670-f7c6-40d0-b80d-c95941a09271)

사용자는 게임내 곡의 리스트를 확인할 수 있으며, 각 곡의 카테고리와 레벨별로 필터를 적용하여 확인 할 수 있습니다.
패턴 파일이 있을 경우 밝은 색으로 표시되고, 패턴 파일이 없을 경우 어두운 색으로 표시되게 해서, 사용자가 구분할 수 있게 했습니다.

![image](https://github.com/Wintiger0222/ez2pattern_server/assets/24960466/5346d1cf-9b7e-47b8-9813-a83a03fb95a9)
채보파일을 불러올 경우 DB내에 저장된 각곡별 레벨, BPM 노트수의 데이터와 각 패턴 별 성격 환산 데이터를 불러와 사용자가 이 곡의 성향을 파악할 수 있게 하였습니다.
또한 게임 내 제공하는 MIRROR, RANDOM 등의 기능을 CSS를 통해 구현하여서 사용자가 게임내 패턴을 미리 볼 수 있게 하였습니다.

## 프로젝트 후기 및 아쉬운 점
해당 프로젝트 전에 서버나 클라이언트 관련 프로그래밍 경험이 전무했습니다. 
해당 프로젝트가 저의 첫 서버 관련 경험 이어가지고 주먹구구식으로 코딩을 하면서 프로젝트를 설계하였습니다.

DB를 얕은 지식에 기반하여 불편한 구조가 되었고, html 렌더링도 보안 이슈 때문에 처음에는 frontend 쪽에서 JS로 렌더링 하는 방향에서 backend에서 미리 랜더링 된 html 코드를 CSS코드와 함께 같이 frontend 로 보내는 방식으로 바꾸었습니다.

또한 검색기능이나 로그인 기능등 사용자가 사용할 수 있는 기술이 누락되어 있으며, nginx 미숙에 의해 간헐적으로 서버가 응답을 못하는 상황이 발생합니다.

처음 하는 서버 관련 프로젝트라는 점에서 이 정도면 잘 만들었다는 생각도 듭니다. 하지만 유지보수 하기에는 불만족이라는 생각이 들며, 이번 프로젝트를 계기로 좀더 체계적인 프로젝트 관리와 기술스택에 대한 이해가 지금이라도 필요하다느 것을 깨닳게 되었습니다.

다음 프로젝트부터는 체계적인 설



## 참고자료
* 점프 투장 고 - https://wikidocs.net/book/4223
* 오라클 클라우드 가입 방법 - https://it.gwangtori.com/40
* 오라클 클라우드 방화벽 설정 - https://kibua20.tistory.com/124
* 파이선 가상환경 설정 - https://stackoverflow.com/questions/46210934/importerror-couldnt-import-django
* 장고 static 파일 자체 호스팅 - https://stackoverflow.com/questions/5836674/why-does-debug-false-setting-make-my-django-static-files-access-fail
* 장고 nginx 연동 - https://nachwon.github.io/django-deploy-3-nginx/
* 장고 uwsgi 연동 - https://jinmay.github.io/2019/03/14/django/
* 장고와 nginx SSL 적용 - https://wikidocs.net/164372
* nginx static 403 오류 - https://stackoverflow.com/questions/16808813/nginx-serve-static-file-and-got-403-forbidden
