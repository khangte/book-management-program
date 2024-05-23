# 도서 관리 프로그램

## 요구사항 분석
- #### 회원(USER)
1.	회원 정보에 회원ID, 이름, 생년월일, 주소, 전화번호, 회원등록일, 대여 권 수를 포함
2.  회원 등록 시 회원id, 이름, 생년월일, 지역, 전화번호를 입력
3.	새로 등록된 회원의 대여 권 수는 ‘0’
4. 	중복된  회원ID는  회원 등록 불가

- #### 도서(BOOK)
1.  도서 정보에 도서번호, 제목, 저자, 가격, 대여가능 여부를 포함 
2.	도서 등록 시 도서번호, 제목, 저자, 가격을 입력
3.	새로 등록된 도서의 대여가능 여부는 ‘Y’
4.	중복된 도서ID는 도서 등록 불가

- #### 대여(RENT)
1.  도서 대여 시 회원ID와 대여할 도서 번호를 입력
2.	도서 개체의 대여가능여부가 ‘Y’ 이면 대여가 가능, 'N’이면 대여 불가
3.	도서 반납 시 반납할 도서 번호를 입력
4.  도서 반납여부가 ‘O’면 반납 완료, ‘X’면 반납 실패
5.	대여가 완료되면 도서 대출일은 당일 날짜, 도서 반납예정일은 도서 대출일 기준 2주 후
6.  대여가 완료되면 회원의 대여 권수 += 1, 대여현황 반납여부 ‘X’ 로 변경
7.	반납이 완료되면 회원의 대여 권수 -= 1, 대여현황 반납여부 ‘O’ 로 변경
<br>

### 릴레이션 키
회원정보 – 회원번호(PK), 이름, 생년월일, 성별, 전화번호, 주소, 메일주소, 등록일, 탈퇴일, 대여 도서권 수  
도서정보 – 도서번호(PK), 도서제목, 저자, 가격. 도서대여 가능여부 
대여정보 – 대여번호(PK), 도서번호(FK), 회원번호(FK), 대출일, 반납 예정일
연체정보 – 회원번호(FK), 연체날짜
<br><Br>

### 회원도서대여 ERD
<img src="https://github.com/khangte/book-management-program/assets/115693185/e1bc9a13-7f98-4c24-b934-1b8785641cb6" width="400" height="300"/>
<br><br>

## MSSQL 쿼리 및 테이블
 ### 회원(USER)
  
  - #### 회원 테이블 쿼리문
```mssql
CREATE TABLE userTbl                            -- 회원 테이블
( USER_ID	CHAR(8) NOT NULL PRIMARY KEY, 	-- 회원 아이디
  USER_NAME	NVARCHAR(10) NOT NULL, 		-- 이름
  USER_BIRTH	DATE NOT NULL, 			-- 생년월일
  USER_ADDR	NCHAR (2) NOT NULL, 	        -- 지역
  USER_PHONE	CHAR(13), 		        -- 휴대폰 번호
  USER_REG_DATE DATE,				-- 회원등록일
  USER_RENT_COUNT 	INT DEFAULT('0')	-- 대여 권수
  );

INSERT INTO userTbl VALUES('KMH', '강민혁', '2000-3-21', '서울', '010-6545-7945', '2019-4-4', 1);
INSERT INTO userTbl VALUES('HYJ', '황예지', '2000-5-26', '전북', '010-1111-1111', '2019-4-21', 0);
INSERT INTO userTbl VALUES('CJS', '최지수', '2000-7-21', '인천', '010-2222-2222', '2019-5-2', 0);
INSERT INTO userTbl VALUES('SRJ', '신류진', '2001-4-17', '강원', '010-3333-3333', '2020-3-13', 0);
INSERT INTO userTbl VALUES('LCR', '이채령', '2001-6-5', '충남', '010-4444-4444' , '2020-7-7', 0);
INSERT INTO userTbl VALUES('SYN', '신유나', '2003-12-9', '강원', '010-5555-5555', '2022-3-21', 1);
```
  - #### 회원 테이블 출력 결과
```mssql
SELECT *  FROM userTbl ORDER BY USER_NAME
```
![image](https://github.com/khangte/book-management-program/assets/115693185/98329a3d-3daa-4e3d-b602-62b09fe7a982)

 ### 도서(BOOK)
   - #### 도서 테이블 쿼리문
```mssql
CREATE TABLE bookTbl 
(
 BOOK_ID INT NOT  NULL PRIMARY  KEY,      -- 도서 번호
 BOOK_TITLE NVARCHAR(20) NOT NULL,	  -- 도서 이름
 BOOK_AUTHOR NVARCHAR(10),		  -- 저자
 BOOK_PRICE INT NOT NULL,		  -- 가격
 BOOK_RENT_YN CHAR(1) NOT NULL	          -- 대여 가능여부
);

INSERT INTO bookTbl VALUES(323, '혼자 공부하는 SQL', '우재남', 24000 ,'Y');
INSERT INTO bookTbl VALUES(144, '데이터베이스 처리', '김성규', 30000 ,'Y');
INSERT INTO bookTbl VALUES(787, '데이터베이스 개론', '김연희', 27000 ,'N');
INSERT INTO bookTbl VALUES(982, 'Java의 정석', '남궁성', 30000 ,'Y');
INSERT INTO bookTbl VALUES(568, '윤성우의 열혈 Java 프로그래밍', '윤성우', 27000 ,'N');
```
   - #### 도서 테이블 출력 결과
```mssql
SELECT * FROM bookTbl
```
![image](https://github.com/khangte/book-management-program/assets/115693185/71bf1c75-807c-4c69-8d18-bdf47a2062d4)

 ### 대여(RENT)
   - #### 대여 테이블 쿼리문
```mssql
CREATE TABLE rentTbl
(	
	USER_ID	CHAR(8) NOT NULL 	--회원 아이디(FK)
			FOREIGN KEY REFERENCES userTbl(USER_ID),
	BOOK_ID INTEGER NOT NULL 	--도서 번호(FK)
			FOREIGN KEY REFERENCES bookTbl(BOOK_ID),
	RENT_DATE DATE,		        -- 도서 대출일
	RENT_RETURN_DATE DATE,	        -- 반납 예정일
	RENT_RETURN_CHECK CHAR(1)	-- 반납 여부
);

INSERT INTO rentTbl VALUES('HYJ', 323, '2022-6-8', '2022-6-22', 'O');
INSERT INTO rentTbl VALUES('SRJ', 982, '2022-11-13', '2022-12-27', 'O');
INSERT INTO rentTbl VALUES('SRJ', 568, '2023-2-11', '2023-2-25', 'O');
INSERT INTO rentTbl VALUES('SYN', 787, '2023-6-1', '2023-6-15', 'X');
INSERT INTO rentTbl VALUES('KMH', 568, '2023-6-3', '2023-6-17', 'X');
```
  - #### 대여 테이블 출력 결과
```mssql
SELECT * FROM  rentTbl
```
![image](https://github.com/khangte/book-management-program/assets/115693185/edb7370b-2c0f-4788-bf2e-2253f88c08d4)

  - #### MSSQL ERD
<img src="https://github.com/khangte/book-management-program/assets/115693185/a1969942-0c3e-4c35-bb6a-103fd775765a" width="400" height="300"/>
<br><br>

## 프로그램 구현 화면
- ### 메인 화면
![image](https://github.com/khangte/book-management-program/assets/115693185/4f33fa75-a41d-4327-810d-4bee2073a436)
<br><br><br>

- ### 회원 정보 구현
![image](https://github.com/khangte/book-management-program/assets/115693185/0bf579cd-ff4b-48a7-a664-b36ea47f1d2c)
![image](https://github.com/khangte/book-management-program/assets/115693185/0bdf1d46-0f19-449b-8cbd-a245f633f8ec)
<br><br><br>

- ### 회원 등록 구현
![image](https://github.com/khangte/book-management-program/assets/115693185/df6d1a1b-57ab-4086-87df-7432e6a9de4e)

등록 성공 ![image](https://github.com/khangte/book-management-program/assets/115693185/b5596d21-8799-4ccc-a729-78e36a480602)   등록 실패 ![image](https://github.com/khangte/book-management-program/assets/115693185/7bac536f-e2c4-4f0c-8055-07ba5064753f)

  - #### 변경 전  ->  변경 후
<img src="https://github.com/khangte/book-management-program/assets/115693185/e29708d8-5fc8-4292-8f19-4fae290359a9" width="400"/>
<img src="https://github.com/khangte/book-management-program/assets/115693185/b9f741ac-7ee4-486d-9a7a-03233f78b6e7" width="400"/>
<img src="https://github.com/khangte/book-management-program/assets/115693185/e059fbf0-8329-4738-bbe0-361244f0279f" width="400"/>
<img src="https://github.com/khangte/book-management-program/assets/115693185/f9ad1c19-8327-4361-b993-11bc695a4219" width="400"/>
<br><br><br>

- ### 도서 목록 구현
![image](https://github.com/khangte/book-management-program/assets/115693185/f69c5b57-7848-4926-89d0-24a022626bbc)
![image](https://github.com/khangte/book-management-program/assets/115693185/bb0177e4-b05d-41c0-8030-107d483bf6d3)
<br><br><Br>

- ### 도서 등록 구현
![image](https://github.com/khangte/book-management-program/assets/115693185/3a089d9a-4c73-40c8-9d76-84db274a1c28)

등록 성공 ![image](https://github.com/khangte/book-management-program/assets/115693185/a74de3f8-d297-42b1-b86f-c40dfa3b993e)
등록 실패 ![image](https://github.com/khangte/book-management-program/assets/115693185/b135891b-d7c5-4b48-af18-29a5f6819c1b)

  - #### 변경 전 -> 변경 후
<img src="https://github.com/khangte/book-management-program/assets/115693185/a75b743c-284a-4ec1-9255-d5002f19a901" width="400"/>
<img src="https://github.com/khangte/book-management-program/assets/115693185/e5b68539-baf0-4bb5-a5a7-2616fd941319" width="400"/>
<img src="https://github.com/khangte/book-management-program/assets/115693185/fdd823c4-ef13-4092-b514-6a429535a446" width="400"/>
<img src="https://github.com/khangte/book-management-program/assets/115693185/acced3a6-553e-4cbf-bccf-91346018cb60" width="400"/>
<br><br><br>

- ### 대여 현황 구현
![image](https://github.com/khangte/book-management-program/assets/115693185/a0bbbedf-bd94-4624-aea7-9f4ac86e8506)
![image](https://github.com/khangte/book-management-program/assets/115693185/89ba7ccb-4d75-4de6-9d63-19097d5d1486)
<br><br><br>

- ### 도서 대여 구현
![image](https://github.com/khangte/book-management-program/assets/115693185/1bb28f30-ee22-4f8c-81dd-21c02bce24cb)

대여 성공 ![image](https://github.com/khangte/book-management-program/assets/115693185/b833308d-34aa-4d22-b1da-b0d4c0960150)
대여 실패 ![image](https://github.com/khangte/book-management-program/assets/115693185/dadc5273-1360-468b-a2e6-9337151f5023)

  - ### 대여 정보
  - #### 변경 전 -> 변경 후
<img src="https://github.com/khangte/book-management-program/assets/115693185/84766699-17d9-4e4c-903f-b7623e4dcbfb" width="400"/>
<img src="https://github.com/khangte/book-management-program/assets/115693185/5c51f945-646c-4648-b0db-80ddb769a28c" width="400"/>
<img src="https://github.com/khangte/book-management-program/assets/115693185/630a143f-5cb0-4aeb-9036-837567c80bb9" width="400"/>
<img src="https://github.com/khangte/book-management-program/assets/115693185/f1ca1483-7b68-47e2-b4c1-c3e91a5960d4" width="400"/>

  - ### 회원정보
  - #### 변경 전 -> 변경 후
<img src="https://github.com/khangte/book-management-program/assets/115693185/4bd765d7-1c4a-414d-b8f6-8cd26bccdd69" width="400"/>
<img src="https://github.com/khangte/book-management-program/assets/115693185/3afe042d-1205-4323-b9d6-021e1cc82e82" width="400"/>
<img src="https://github.com/khangte/book-management-program/assets/115693185/805af9ab-0b4a-409b-be48-b0605fe5950c" width="400"/>
<img src="https://github.com/khangte/book-management-program/assets/115693185/477665f9-d7f2-4691-8e9c-08d80c81af8a" width="400"/>

  - ### 도서목록
  - #### 변경 전 -> 변경 후
<img src="https://github.com/khangte/book-management-program/assets/115693185/b346190d-2b02-4c6a-a22c-f68193747f81" width="400"/>
<img src="https://github.com/khangte/book-management-program/assets/115693185/559235f0-686f-4bba-bc26-fdc4416325a3" width="400"/>
<img src="https://github.com/khangte/book-management-program/assets/115693185/ed5b62b6-5205-49fe-8ec7-5814906163e8" width="400"/>
<img src="https://github.com/khangte/book-management-program/assets/115693185/4bdd0596-e84c-49bd-b179-fa6fef289df5" width="400"/>
<br><br><br>

- ### 도서 반납 구현
![image](https://github.com/khangte/book-management-program/assets/115693185/43f53518-37f9-4aff-8f08-36b9d90b1fdd)
<br>
반납 성공 ![image](https://github.com/khangte/book-management-program/assets/115693185/6d5b4363-5881-4b24-b5ea-0b832f8522cf)
반납 실패 ![image](https://github.com/khangte/book-management-program/assets/115693185/1cce842e-212f-467a-a46d-31d2793854ce)

  - #### 변경 전 -> 변경 후
<img src="https://github.com/khangte/book-management-program/assets/115693185/b67e2fc6-7668-47e6-b96b-3fdc3ddce758" width="400"/>
<img src="https://github.com/khangte/book-management-program/assets/115693185/14817c74-a73c-4703-87ce-3c3c3cf883be" width="400"/>
<img src="https://github.com/khangte/book-management-program/assets/115693185/a78d475c-7fcf-4c34-b114-173215dbc752" width="400"/>
<img src="https://github.com/khangte/book-management-program/assets/115693185/009ed501-052f-404e-839c-ba5eecc2741a" width="400"/>

  - ### 회원 정보
  - #### 변경 전 -> 변경 후
<img src="https://github.com/khangte/book-management-program/assets/115693185/97c33c7a-52bd-47aa-9279-1bf5737e187c" width="400"/>
<img src="https://github.com/khangte/book-management-program/assets/115693185/1690f581-cdd6-419a-9be3-74eb8e6fd30b" width="400"/>

  - ### 도서 정보
  - #### 변경 전 -> 변경 후
<img src="https://github.com/khangte/book-management-program/assets/115693185/6327eb6d-9178-4c67-aac7-1b5684d3b524" width="400"/>
<img src="https://github.com/khangte/book-management-program/assets/115693185/e43b581a-877e-4c01-9126-58f66ff5c801" width="400"/>
