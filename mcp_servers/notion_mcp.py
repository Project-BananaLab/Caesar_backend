"""
Notion MCP 서버 연결 모듈
통합 테스트에서 사용되는 기능들을 포함합니다.
"""

import os
from typing import Dict, Any, List, Optional
import asyncio


class NotionMCP:
    """Notion MCP 서버 연결 클래스"""

    def __init__(self, token: str = None):
        self.token = token or os.getenv("NOTION_TOKEN")
        self.client = None
        self.connected = False

    async def connect(self) -> bool:
        """MCP 서버 연결 (Smithery 프록시 사용)"""
        try:
            print("Notion MCP 서버에 연결 중... (Smithery 프록시)")
            # 시뮬레이션된 연결
            await asyncio.sleep(0.1)
            self.connected = True
            print("✅ Notion MCP 서버 연결 성공 (Smithery 프록시)")
            return True
        except Exception as e:
            print(f"Notion 연결 실패: {e}")
            return False

    async def disconnect(self):
        """MCP 서버 연결 해제"""
        self.connected = False
        print("Notion MCP 서버 연결 해제")

    async def get_available_tools(self) -> List[str]:
        """사용 가능한 도구 목록 조회"""
        if not self.connected:
            raise Exception("연결되지 않음")

        await asyncio.sleep(0.1)

        # Smithery를 통해 사용 가능한 Notion 도구들
        tools = [
            "notion_query_database",
            "notion_create_page",
            "notion_update_page",
            "notion_delete_page",
            "notion_search",
            "notion_append_block",
            "notion_get_page",
            "notion_get_database",
            "notion_create_database",
            "notion_list_users",
            "notion_get_block_children",
        ]

        return tools

    async def call_custom_tool(
        self, tool_name: str, **kwargs
    ) -> Optional[Dict[str, Any]]:
        """커스텀 도구 호출"""
        if not self.connected:
            raise Exception("연결되지 않음")

        await asyncio.sleep(0.2)

        if tool_name == "notion_status":
            return {
                "status": "connected",
                "proxy": "Smithery",
                "api_version": "2022-06-28",
            }

        return None

    async def query_database(
        self, database_id: str, filter_conditions: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """데이터베이스 쿼리"""
        if not self.connected:
            raise Exception("연결되지 않음")

        await asyncio.sleep(0.3)

        # 시뮬레이션된 데이터베이스 결과
        results = [
            {
                "id": "page1",
                "object": "page",
                "created_time": "2024-01-15T10:30:00.000Z",
                "properties": {
                    "Name": {"title": [{"text": {"content": "샘플 페이지 1"}}]},
                    "Status": {"select": {"name": "진행 중"}},
                },
            },
            {
                "id": "page2",
                "object": "page",
                "created_time": "2024-01-14T14:20:00.000Z",
                "properties": {
                    "Name": {"title": [{"text": {"content": "샘플 페이지 2"}}]},
                    "Status": {"select": {"name": "완료"}},
                },
            },
        ]

        return results

    async def create_page(
        self,
        parent_id: str,
        properties: Dict[str, Any],
        content: List[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """페이지 생성"""
        if not self.connected:
            raise Exception("연결되지 않음")

        await asyncio.sleep(0.4)

        return {
            "id": f"page_{hash(str(properties)) % 1000000}",
            "object": "page",
            "created_time": "2024-01-15T12:00:00.000Z",
            "properties": properties,
            "url": f"https://notion.so/page_{hash(str(properties)) % 1000000}",
        }

    async def update_page(
        self, page_id: str, properties: Dict[str, Any]
    ) -> Dict[str, Any]:
        """페이지 수정"""
        if not self.connected:
            raise Exception("연결되지 않음")

        await asyncio.sleep(0.3)

        return {
            "id": page_id,
            "object": "page",
            "last_edited_time": "2024-01-15T12:30:00.000Z",
            "properties": properties,
        }

    async def delete_page(self, page_id: str) -> bool:
        """페이지 삭제"""
        if not self.connected:
            raise Exception("연결되지 않음")

        await asyncio.sleep(0.2)
        return True

    async def search(self, query: str, filter_type: str = None) -> List[Dict[str, Any]]:
        """검색"""
        if not self.connected:
            raise Exception("연결되지 않음")

        await asyncio.sleep(0.3)

        # 시뮬레이션된 검색 결과
        results = [
            {
                "id": "search_result_1",
                "object": "page",
                "created_time": "2024-01-15T10:00:00.000Z",
                "properties": {
                    "title": {
                        "title": [{"text": {"content": f"'{query}' 검색 결과 1"}}]
                    }
                },
                "url": "https://notion.so/search_result_1",
            },
            {
                "id": "search_result_2",
                "object": "page",
                "created_time": "2024-01-14T15:30:00.000Z",
                "properties": {
                    "title": {
                        "title": [{"text": {"content": f"'{query}' 관련 페이지"}}]
                    }
                },
                "url": "https://notion.so/search_result_2",
            },
        ]

        return results

    async def append_block(self, page_id: str, blocks: List[Dict[str, Any]]) -> bool:
        """블록 추가"""
        if not self.connected:
            raise Exception("연결되지 않음")

        await asyncio.sleep(0.3)
        return True

    async def get_page(self, page_id: str) -> Dict[str, Any]:
        """페이지 정보 조회"""
        if not self.connected:
            raise Exception("연결되지 않음")

        await asyncio.sleep(0.2)

        return {
            "id": page_id,
            "object": "page",
            "created_time": "2024-01-15T10:00:00.000Z",
            "last_edited_time": "2024-01-15T12:00:00.000Z",
            "properties": {"title": {"title": [{"text": {"content": "샘플 페이지"}}]}},
            "url": f"https://notion.so/{page_id}",
        }

    async def get_database(self, database_id: str) -> Dict[str, Any]:
        """데이터베이스 정보 조회"""
        if not self.connected:
            raise Exception("연결되지 않음")

        await asyncio.sleep(0.2)

        return {
            "id": database_id,
            "object": "database",
            "created_time": "2024-01-10T09:00:00.000Z",
            "title": [{"text": {"content": "샘플 데이터베이스"}}],
            "properties": {
                "Name": {"title": {}},
                "Status": {
                    "select": {"options": [{"name": "진행 중"}, {"name": "완료"}]}
                },
            },
            "url": f"https://notion.so/{database_id}",
        }
