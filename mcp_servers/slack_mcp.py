"""
Slack MCP 서버 연결 모듈
실제 Slack Web API와 연동하여 작동합니다.
"""

import os
from typing import Dict, Any, List, Optional
import asyncio
import aiohttp
import json


class SlackMCP:
    """Slack MCP 서버 연결 클래스"""

    def __init__(self, token: str = None):
        self.token = token or os.getenv("SLACK_BOT_TOKEN")
        self.client = None
        self.connected = False
        self.base_url = "https://slack.com/api"
        self.session = None

    async def connect(self) -> bool:
        """MCP 서버 연결"""
        try:
            if not self.token:
                print("❌ SLACK_BOT_TOKEN이 설정되지 않았습니다.")
                return False

            print("Slack MCP 서버에 연결 중...")

            # aiohttp 세션 생성
            self.session = aiohttp.ClientSession()

            # 토큰 검증 (auth.test API 호출)
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            }

            async with self.session.get(
                f"{self.base_url}/auth.test", headers=headers
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("ok"):
                        self.connected = True
                        print(
                            f"✅ Slack MCP 서버 연결 성공 - 팀: {data.get('team', 'Unknown')}"
                        )
                        return True
                    else:
                        print(
                            f"❌ Slack 인증 실패: {data.get('error', 'Unknown error')}"
                        )
                        return False
                else:
                    print(f"❌ Slack API 호출 실패: HTTP {response.status}")
                    return False

        except Exception as e:
            print(f"Slack 연결 실패: {e}")
            if self.session:
                await self.session.close()
                self.session = None
            return False

    async def disconnect(self):
        """MCP 서버 연결 해제"""
        self.connected = False
        if self.session:
            await self.session.close()
            self.session = None
        print("Slack MCP 서버 연결 해제")

    async def _api_call(
        self, method: str, data: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Slack API 호출 헬퍼 메서드"""
        if not self.connected or not self.session:
            raise Exception("연결되지 않음")

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

        url = f"{self.base_url}/{method}"

        try:
            if data:
                async with self.session.post(
                    url, headers=headers, json=data
                ) as response:
                    return await response.json()
            else:
                async with self.session.get(url, headers=headers) as response:
                    return await response.json()
        except Exception as e:
            raise Exception(f"API 호출 실패: {e}")

    async def get_available_tools(self) -> List[str]:
        """사용 가능한 도구 목록 조회"""
        if not self.connected:
            raise Exception("연결되지 않음")

        # 실제 사용 가능한 도구 목록
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

        try:
            # 공개 채널 목록 조회
            response = await self._api_call(
                "conversations.list",
                {"types": "public_channel,private_channel", "exclude_archived": True},
            )

            if not response.get("ok"):
                raise Exception(
                    f"채널 목록 조회 실패: {response.get('error', 'Unknown error')}"
                )

            channels = []
            for channel in response.get("channels", []):
                channels.append(
                    {
                        "id": channel.get("id"),
                        "name": channel.get("name"),
                        "is_private": channel.get("is_private", False),
                        "members": channel.get("num_members", 0),
                        "purpose": channel.get("purpose", {}).get("value", ""),
                        "topic": channel.get("topic", {}).get("value", ""),
                        "created": channel.get("created", 0),
                    }
                )

            return channels

        except Exception as e:
            raise Exception(f"채널 목록 조회 중 오류: {e}")

    async def send_message(
        self, channel: str, text: str, blocks: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """메시지 전송"""
        if not self.connected:
            raise Exception("연결되지 않음")

        try:
            data = {"channel": channel, "text": text}

            if blocks:
                data["blocks"] = blocks

            response = await self._api_call("chat.postMessage", data)

            if not response.get("ok"):
                raise Exception(
                    f"메시지 전송 실패: {response.get('error', 'Unknown error')}"
                )

            return response

        except Exception as e:
            raise Exception(f"메시지 전송 중 오류: {e}")

    async def get_channel_history(
        self, channel: str, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """채널 히스토리 조회"""
        if not self.connected:
            raise Exception("연결되지 않음")

        try:
            response = await self._api_call(
                "conversations.history", {"channel": channel, "limit": limit}
            )

            if not response.get("ok"):
                raise Exception(
                    f"채널 히스토리 조회 실패: {response.get('error', 'Unknown error')}"
                )

            return response.get("messages", [])

        except Exception as e:
            raise Exception(f"채널 히스토리 조회 중 오류: {e}")

    async def create_channel(
        self, name: str, is_private: bool = False
    ) -> Dict[str, Any]:
        """채널 생성"""
        if not self.connected:
            raise Exception("연결되지 않음")

        try:
            method = "conversations.create"
            data = {"name": name, "is_private": is_private}

            response = await self._api_call(method, data)

            if not response.get("ok"):
                raise Exception(
                    f"채널 생성 실패: {response.get('error', 'Unknown error')}"
                )

            return response

        except Exception as e:
            raise Exception(f"채널 생성 중 오류: {e}")

    async def invite_to_channel(self, channel: str, users: List[str]) -> bool:
        """채널 초대"""
        if not self.connected:
            raise Exception("연결되지 않음")

        try:
            for user in users:
                response = await self._api_call(
                    "conversations.invite", {"channel": channel, "users": user}
                )

                if not response.get("ok"):
                    raise Exception(
                        f"사용자 초대 실패: {response.get('error', 'Unknown error')}"
                    )

            return True

        except Exception as e:
            raise Exception(f"채널 초대 중 오류: {e}")

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

        try:
            data = {
                "channels": ",".join(channels),
                "title": title or os.path.basename(file_path),
                "initial_comment": comment,
            }

            # 실제 파일 업로드는 multipart form을 사용해야 하므로 간소화
            response = await self._api_call("files.upload", data)

            if not response.get("ok"):
                raise Exception(
                    f"파일 업로드 실패: {response.get('error', 'Unknown error')}"
                )

            return response

        except Exception as e:
            raise Exception(f"파일 업로드 중 오류: {e}")

    async def set_status(self, text: str, emoji: str = None) -> bool:
        """상태 설정"""
        if not self.connected:
            raise Exception("연결되지 않음")

        try:
            profile = {"status_text": text}
            if emoji:
                profile["status_emoji"] = emoji

            response = await self._api_call("users.profile.set", {"profile": profile})

            if not response.get("ok"):
                raise Exception(
                    f"상태 설정 실패: {response.get('error', 'Unknown error')}"
                )

            return True

        except Exception as e:
            raise Exception(f"상태 설정 중 오류: {e}")

    async def get_user_info(self, user_id: str) -> Dict[str, Any]:
        """사용자 정보 조회"""
        if not self.connected:
            raise Exception("연결되지 않음")

        try:
            response = await self._api_call("users.info", {"user": user_id})

            if not response.get("ok"):
                raise Exception(
                    f"사용자 정보 조회 실패: {response.get('error', 'Unknown error')}"
                )

            return response

        except Exception as e:
            raise Exception(f"사용자 정보 조회 중 오류: {e}")

    async def search_messages(
        self, query: str, count: int = 20
    ) -> List[Dict[str, Any]]:
        """메시지 검색"""
        if not self.connected:
            raise Exception("연결되지 않음")

        try:
            response = await self._api_call(
                "search.messages", {"query": query, "count": count}
            )

            if not response.get("ok"):
                raise Exception(
                    f"메시지 검색 실패: {response.get('error', 'Unknown error')}"
                )

            messages = response.get("messages", {})
            return messages.get("matches", [])

        except Exception as e:
            raise Exception(f"메시지 검색 중 오류: {e}")
