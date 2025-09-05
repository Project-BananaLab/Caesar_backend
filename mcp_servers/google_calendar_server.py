"""
Google Calendar MCP 서버 연결 모듈
통합 테스트에서 사용되는 기능들을 포함합니다.
"""

import os
from typing import Dict, Any, List, Optional
from datetime import datetime
import asyncio


class GoogleCalendarServer:
    """Google Calendar MCP 서버 연결 클래스"""

    def __init__(self, credentials_path: str = None):
        self.credentials_path = credentials_path or os.getenv(
            "GOOGLE_CALENDAR_CREDENTIALS"
        )
        self.client = None
        self.connected = False

    async def connect(self) -> bool:
        """MCP 서버 연결"""
        try:
            print("Google Calendar MCP 서버에 연결 중...")
            await asyncio.sleep(0.1)
            self.connected = True
            print("✅ Google Calendar MCP 서버 연결 성공")
            return True
        except Exception as e:
            print(f"Google Calendar 연결 실패: {e}")
            return False

    async def disconnect(self):
        """MCP 서버 연결 해제"""
        self.connected = False
        print("Google Calendar MCP 서버 연결 해제")

    async def list_calendars(self) -> List[Dict[str, Any]]:
        """캘린더 목록 조회"""
        if not self.connected:
            raise Exception("연결되지 않음")

        await asyncio.sleep(0.2)

        # 시뮬레이션된 캘린더 목록
        calendars = [
            {
                "id": "primary",
                "summary": "개인 캘린더",
                "primary": True,
                "accessRole": "owner",
            },
            {
                "id": "work@example.com",
                "summary": "업무 캘린더",
                "primary": False,
                "accessRole": "owner",
            },
            {
                "id": "team@example.com",
                "summary": "팀 캘린더",
                "primary": False,
                "accessRole": "writer",
            },
        ]

        return calendars

    async def list_events(
        self,
        calendar_id: str = "primary",
        time_min: datetime = None,
        time_max: datetime = None,
        max_results: int = 10,
    ) -> List[Dict[str, Any]]:
        """이벤트 목록 조회"""
        if not self.connected:
            raise Exception("연결되지 않음")

        await asyncio.sleep(0.2)

        # 시뮬레이션된 이벤트 목록
        events = [
            {
                "id": "event1",
                "summary": "팀 미팅",
                "start": {"dateTime": "2024-01-15T10:00:00Z"},
                "end": {"dateTime": "2024-01-15T11:00:00Z"},
                "description": "주간 팀 미팅입니다.",
            },
            {
                "id": "event2",
                "summary": "프로젝트 리뷰",
                "start": {"dateTime": "2024-01-15T14:00:00Z"},
                "end": {"dateTime": "2024-01-15T15:00:00Z"},
                "description": "Caesar 프로젝트 진행 상황 리뷰",
            },
            {
                "id": "event3",
                "summary": "클라이언트 미팅",
                "start": {"dateTime": "2024-01-16T09:00:00Z"},
                "end": {"dateTime": "2024-01-16T10:30:00Z"},
                "description": "새로운 요구사항 논의",
            },
        ]

        return events[:max_results]

    async def create_event(
        self,
        summary: str,
        start_time: datetime,
        end_time: datetime,
        description: str = None,
        attendees: List[str] = None,
    ) -> Dict[str, Any]:
        """이벤트 생성"""
        if not self.connected:
            raise Exception("연결되지 않음")

        await asyncio.sleep(0.3)

        return {
            "id": f"event_{hash(summary) % 1000000}",
            "summary": summary,
            "description": description,
            "start": {"dateTime": start_time.isoformat()},
            "end": {"dateTime": end_time.isoformat()},
            "status": "confirmed",
        }

    async def update_event(
        self, event_id: str, updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """이벤트 수정"""
        if not self.connected:
            raise Exception("연결되지 않음")

        await asyncio.sleep(0.3)
        return {"id": event_id, "status": "confirmed", **updates}

    async def delete_event(self, event_id: str) -> bool:
        """이벤트 삭제"""
        if not self.connected:
            raise Exception("연결되지 않음")

        await asyncio.sleep(0.2)
        return True

    async def find_free_time(
        self, duration_minutes: int, time_min: datetime, time_max: datetime
    ) -> List[Dict[str, Any]]:
        """빈 시간 찾기"""
        if not self.connected:
            raise Exception("연결되지 않음")

        await asyncio.sleep(0.3)

        # 시뮬레이션된 빈 시간 슬롯
        free_slots = [
            {"start": "2024-01-15T12:00:00Z", "end": "2024-01-15T13:00:00Z"},
            {"start": "2024-01-15T16:00:00Z", "end": "2024-01-15T17:30:00Z"},
        ]

        return free_slots
