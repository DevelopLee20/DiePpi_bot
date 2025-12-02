import logging

import discord
from discord.ext import commands

from cogs.base_cog import BaseCog
from core.env import env
from core.messages import weekly_stats_message
from db.study_collection import StudyCollection

logger = logging.getLogger(__name__)


class WeekAnalytics(BaseCog):
    """주간 공부 통계를 제공하는 Cog."""

    def __init__(self, bot: commands.Bot) -> None:
        """WeekAnalytics 초기화.

        Args:
            bot: Discord bot 인스턴스
        """
        super().__init__(bot)

    @commands.hybrid_command(name="주간공부", description="주간 공부 통계를 조회합니다")
    async def weekly_study_stats(
        self, ctx: commands.Context, member: discord.Member | None = None
    ) -> None:
        """주간 공부 통계를 조회합니다.

        Args:
            ctx: Discord 명령어 컨텍스트
            member: 조회할 사용자 (기본값: 명령어 사용자)
        """
        try:
            # 기본값: 명령어 사용자 본인
            target_member = member or ctx.author
            user_id = str(target_member.id)

            # slash command인 경우만 defer 처리
            if ctx.interaction:
                await ctx.interaction.response.defer(thinking=True)

            # 주간 공부 데이터 조회
            daily_stats = await StudyCollection.get_weekly_study_by_user(user_id)

            # 총 공부 시간 계산
            total_min = sum(stat["total_min"] for stat in daily_stats)

            # Gemini API를 통해 평가 메시지 생성
            gemini_client = self.bot.get_gemini_client(
                env.GEMINI_WEEKLY_EVALUATION_INSTRUCTION
            )
            input_text = f"총 공부시간: {total_min // 60}시간 {total_min % 60}분"
            status_code, evaluation = await gemini_client.create_gemini_message(
                input_text
            )

            if not status_code:
                # API 호출 실패 시 에러 메시지 사용
                evaluation = "죄송하다 삐… Gemini 응답에 실패했다 삐!"

            # 메시지 생성
            message = weekly_stats_message(
                target_member.name, daily_stats, total_min, evaluation
            )

            # Discord에 전송
            await ctx.send(message)
        except discord.errors.HTTPException as e:
            logger.error(f"Discord HTTP 오류: {e}")
            try:
                await ctx.send("응답을 보내는 중 오류가 발생했다 삐!")
            except Exception:
                pass
        except Exception as e:
            logger.error(f"주간 공부 통계 조회 중 오류 발생: {e}", exc_info=True)
            try:
                await ctx.send(
                    "주간 공부 통계 조회 중 오류가 발생했습니다. 나중에 다시 시도해주세요."
                )
            except Exception:
                pass


async def setup(bot):
    await bot.add_cog(WeekAnalytics(bot))
