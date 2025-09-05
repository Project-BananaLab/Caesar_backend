"""
Slack MCP 서버 연결 모듈
통합 테스트에서 사용되는 기능들을 포함합니다.
"""

import os
from typing import Dict, Any, List, Optional
import asyncio


class SlackMCP:
    """Slack MCP 서버 연결 클래스"""

    def __init__(self, token: str = None):
        self.token = token or os.getenv("SLACK_BOT_TOKEN")
        self.client = None
        self.connected = False

    async def connect(self) -> bool:
        """MCP 서버 연결"""
        try:
            if not self.token:
                print("❌ SLACK_BOT_TOKEN이 설정되지 않았습니다.")
                return False

            print("Slack MCP 서버에 연결 중...")
            # 시뮬레이션된 연결
            await asyncio.sleep(0.1)
            self.connected = True
            print("✅ Slack MCP 서버 연결 성공")
            return True
        except Exception as e:
            print(f"Slack 연결 실패: {e}")
            return False

    async def disconnect(self):
        """MCP 서버 연결 해제"""
        self.connected = False
        print("Slack MCP 서버 연결 해제")

    async def get_available_tools(self) -> List[str]:
        """사용 가능한 도구 목록 조회"""
        if not self.connected:
            raise Exception("연결되지 않음")

        await asyncio.sleep(0.1)

        # 시뮬레이션된 도구 목록
        tools = [
            "slack_send_message",
            "slack_list_channels",
            "slack_get_channel_history",
            "slack_create_channel",
            "slack_invite_to_channel",
            "slack_upload_file",
            "slack_set_status",
            "slack_get_user_info",
            "slack_search_messages",
            "slack_pin_message",
            "slack_react_to_message",
            "slack_schedule_message",
        ]

        return tools

    async def list_channels(self) -> List[Dict[str, Any]]:
        """채널 목록 조회"""
        if not self.connected:
            raise Exception("연결되지 않음")

        await asyncio.sleep(0.2)

        # 시뮬레이션된 채널 목록
        channels = [
            {
                "id": "C1234567890",
                "name": "general",
                "is_private": False,
                "members": 15,
                "purpose": "전체 공지사항 및 일반적인 대화",
            },
            {
                "id": "C2345678901",
                "name": "development",
                "is_private": False,
                "members": 8,
                "purpose": "개발 관련 논의",
            },
            {
                "id": "C3456789012",
                "name": "caesar-ai",
                "is_private": False,
                "members": 5,
                "purpose": "Caesar AI 프로젝트 관련",
            },
            {
                "id": "C4567890123",
                "name": "random",
                "is_private": False,
                "members": 12,
                "purpose": "자유로운 대화",
            },
        ]

        return channels

    async def send_message(
        self, channel: str, text: str, blocks: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """메시지 전송"""
        if not self.connected:
            raise Exception("연결되지 않음")

        await asyncio.sleep(0.2)

        return {
            "ok": True,
            "channel": channel,
            "ts": "1640995200.123456",
            "message": {
                "type": "message",
                "user": "U1234567890",
                "text": text,
                "ts": "1640995200.123456",
            },
        }

    async def get_channel_history(
        self, channel: str, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """채널 히스토리 조회"""
        if not self.connected:
            raise Exception("연결되지 않음")

        await asyncio.sleep(0.3)

        # 시뮬레이션된 메시지 히스토리
        messages = [
            {
                "type": "message",
                "user": "U1234567890",
                "text": "안녕하세요! Caesar AI 테스트 중입니다.",
                "ts": "1640995200.123456",
            },
            {
                "type": "message",
                "user": "U2345678901",
                "text": "테스트가 잘 진행되고 있나요?",
                "ts": "1640995260.123457",
            },
            {
                "type": "message",
                "user": "U1234567890",
                "text": "네, 모든 기능이 정상적으로 작동하고 있습니다!",
                "ts": "1640995320.123458",
            },
        ]

        return messages[:limit]

    async def create_channel(
        self, name: str, is_private: bool = False
    ) -> Dict[str, Any]:
        """채널 생성"""
        if not self.connected:
            raise Exception("연결되지 않음")

        await asyncio.sleep(0.3)

        return {
            "ok": True,
            "channel": {
                "id": f"C{hash(name) % 1000000000}",
                "name": name,
                "is_private": is_private,
                "created": 1640995200,
            },
        }

    async def invite_to_channel(self, channel: str, users: List[str]) -> bool:
        """채널 초대"""
        if not self.connected:
            raise Exception("연결되지 않음")

        await asyncio.sleep(0.2)
        return True

    async def upload_file(
        self,
        channels: List[str],
        file_path: str,
        title: str = None,
        comment: str = None,
    ) -> Dict[str, Any]:
        """파일 업로드"""
        if not self.connected:
            raise Exception("연결되지 않음")

        await asyncio.sleep(0.4)

        file_name = os.path.basename(file_path)
        return {
            "ok": True,
            "file": {
                "id": f"F{hash(file_path) % 1000000000}",
                "name": file_name,
                "title": title or file_name,
                "mimetype": "application/octet-stream",
                "size": 1024,
                "url_private": f"https://files.slack.com/files-pri/TEAM-FILE/{file_name}",
            },
        }

    async def set_status(self, text: str, emoji: str = None) -> bool:
        """상태 설정"""
        if not self.connected:
            raise Exception("연결되지 않음")

        await asyncio.sleep(0.1)
        return True

    async def get_user_info(self, user_id: str) -> Dict[str, Any]:
        """사용자 정보 조회"""
        if not self.connected:
            raise Exception("연결되지 않음")

        await asyncio.sleep(0.2)

        return {
            "ok": True,
            "user": {
                "id": user_id,
                "name": "testuser",
                "real_name": "Test User",
                "profile": {
                    "display_name": "Test User",
                    "email": "test@example.com",
                    "image_24": "https://example.com/avatar.jpg",
                },
            },
        }

    async def search_messages(
        self, query: str, count: int = 20
    ) -> List[Dict[str, Any]]:
        """메시지 검색"""
        if not self.connected:
            raise Exception("연결되지 않음")

        await asyncio.sleep(0.3)

        # 시뮬레이션된 검색 결과
        results = [
            {
                "type": "message",
                "user": "U1234567890",
                "text": f"'{query}' 관련 메시지입니다.",
                "ts": "1640995200.123456",
                "channel": "C1234567890",
            }
        ]

        return results[:count]
