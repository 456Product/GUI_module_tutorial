# GUI 
 GUI 연습 폴더입니다.
 
### pycharm 패키지 설치
```File - settings - Project:## - Project interpreter - [+] - package 선택```


### 기본적인 모듈 구조
```
app.py
file.py
module (폴더)
ㄴ __init__.py
ㄴ test.py
```

1. 같은 폴더에서 
   1) file.py 호출 : ```import file```
   1) modul(폴더)호출 : ```import module```

1. 폴더를 모듈로 인식시키기 : 
    1)module 폴더 안에 ```__init__.py``` 생성

1. 해당 모듈의 ```__init__.py``` 호출
   1) ```import module```
   1) ```from module import *``` 모두 가져오지 않음

1. test.py 호출
   1) 모듈의 ```__init__.py```에서 ```import test```
   2) app에서 ```from module import test```
   3) app에서 ```import module.test```
   
이떄 ii,iii는 module.__init__ 호출 후 test를 호출한다.


## 함수 호출의 3가지 방법

### 1. 모듈 이름으로 호출.
```
import App
App.module.test_file.test1()
```

위의 코드는 App만 import 했다. 따라서 App을 통해서만 다른 파일에 접근할 수 있다.
App이 module을 import 하고 있으므로 App을 통해 module에 접근한다. App.module
현재 폴더 구조는 module(폴더)에 test_file.py가 test1() 함수를 포함하고 있다. 차례대로 불러준다.
App.module.test_file.test1()

### 2. 모듈을 변수에 저장해서 호출
```
import module.test_file as a
print(type(a))
a.test1()
```
이떄 주의할 것은 App은 package(폴더)가 아니기 때문에 App.module을 쓸 수 없다는 것이다.


### 3. 함수명을 바로 꺼내서 쓰는법
```
from module.test_file import *     # 전체 불러오기
from module.test_file import test1 # 사용할 함수만 불러오기
test1()
```
module 폴더에 test_file까지 접근한 후 모든(*) class와 function을 import 한다.
해당 모듈의 내용물을 몽땅 이 파일로 불러왔기 때문에 (복잡한 경로 없이) 바로 함수 이름으로 호출할 수 있다.

