"""
Google Drive MCP 서버 연결 모듈
통합 테스트에서 사용되는 기능들을 포함합니다.
"""

import os
from typing import Dict, Any, List, Optional
import asyncio


class GoogleDriveMCP:
    """Google Drive MCP 서버 연결 클래스"""

    def __init__(self, credentials_path: str = None):
        self.credentials_path = credentials_path or os.getenv(
            "GOOGLE_DRIVE_CREDENTIALS"
        )
        self.client = None
        self.connected = False

    async def connect(self) -> bool:
        """MCP 서버 연결"""
        try:
            print("Google Drive MCP 서버에 연결 중...")
            # 시뮬레이션된 연결
            await asyncio.sleep(0.1)
            self.connected = True
            print("✅ Google Drive MCP 서버 연결 성공")
            return True
        except Exception as e:
            print(f"Google Drive 연결 실패: {e}")
            return False

    async def disconnect(self):
        """MCP 서버 연결 해제"""
        self.connected = False
        print("Google Drive MCP 서버 연결 해제")

    async def list_files(
        self, folder_id: str = None, max_results: int = 10
    ) -> List[Dict[str, Any]]:
        """파일 목록 조회"""
        if not self.connected:
            raise Exception("연결되지 않음")

        # 시뮬레이션된 파일 목록
        await asyncio.sleep(0.2)
        sample_files = [
            {
                "id": "1ABC123def456",
                "name": "문서1.docx",
                "mimeType": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                "createdTime": "2024-01-15T10:30:00.000Z",
                "size": "524288",
            },
            {
                "id": "2DEF456ghi789",
                "name": "스프레드시트1.xlsx",
                "mimeType": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "createdTime": "2024-01-14T14:20:00.000Z",
                "size": "1048576",
            },
            {
                "id": "3GHI789jkl012",
                "name": "프레젠테이션1.pptx",
                "mimeType": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
                "createdTime": "2024-01-13T09:15:00.000Z",
                "size": "2097152",
            },
            {
                "id": "4JKL012mno345",
                "name": "이미지1.jpg",
                "mimeType": "image/jpeg",
                "createdTime": "2024-01-12T16:45:00.000Z",
                "size": "3145728",
            },
            {
                "id": "5MNO345pqr678",
                "name": "텍스트파일.txt",
                "mimeType": "text/plain",
                "createdTime": "2024-01-11T11:30:00.000Z",
                "size": "4096",
            },
        ]

        return sample_files[:max_results]

    async def get_file_info(self, file_id: str) -> Optional[Dict[str, Any]]:
        """파일 정보 조회"""
        if not self.connected:
            raise Exception("연결되지 않음")

        await asyncio.sleep(0.1)

        # 시뮬레이션된 파일 정보
        file_info = {
            "id": file_id,
            "name": "샘플파일.docx",
            "mimeType": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "size": "524288",
            "createdTime": "2024-01-15T10:30:00.000Z",
            "modifiedTime": "2024-01-15T15:45:00.000Z",
            "owners": [{"displayName": "사용자", "emailAddress": "user@example.com"}],
            "webViewLink": f"https://docs.google.com/document/d/{file_id}/edit",
        }

        return file_info

    async def search_files(
        self, query: str, max_results: int = 10
    ) -> List[Dict[str, Any]]:
        """파일 검색"""
        if not self.connected:
            raise Exception("연결되지 않음")

        await asyncio.sleep(0.3)

        # 시뮬레이션된 검색 결과
        search_results = [
            {
                "id": "search1",
                "name": f"{query}_결과1.docx",
                "mimeType": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                "snippet": f"'{query}' 검색어와 관련된 내용이 포함된 문서입니다.",
            },
            {
                "id": "search2",
                "name": f"{query}_결과2.xlsx",
                "mimeType": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "snippet": f"'{query}' 키워드가 포함된 스프레드시트입니다.",
            },
            {
                "id": "search3",
                "name": f"{query}_관련파일.txt",
                "mimeType": "text/plain",
                "snippet": f"'{query}' 검색 조건에 맞는 텍스트 파일입니다.",
            },
        ]

        return search_results[:max_results]

    async def upload_file(
        self, file_path: str, folder_id: str = None
    ) -> Dict[str, Any]:
        """파일 업로드"""
        if not self.connected:
            raise Exception("연결되지 않음")

        await asyncio.sleep(0.5)

        file_name = os.path.basename(file_path)
        return {
            "id": f"upload_{hash(file_path) % 10000}",
            "name": file_name,
            "webViewLink": f"https://drive.google.com/file/d/upload_{hash(file_path) % 10000}/view",
        }

    async def download_file(self, file_id: str, local_path: str) -> bool:
        """파일 다운로드"""
        if not self.connected:
            raise Exception("연결되지 않음")

        await asyncio.sleep(0.4)
        return True

    async def create_folder(self, name: str, parent_id: str = None) -> Dict[str, Any]:
        """폴더 생성"""
        if not self.connected:
            raise Exception("연결되지 않음")

        await asyncio.sleep(0.2)
        return {
            "id": f"folder_{hash(name) % 10000}",
            "name": name,
            "mimeType": "application/vnd.google-apps.folder",
        }

    async def share_file(self, file_id: str, email: str, role: str = "reader") -> bool:
        """파일 공유"""
        if not self.connected:
            raise Exception("연결되지 않음")

        await asyncio.sleep(0.3)
        return True
