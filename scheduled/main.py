from apscheduler.schedulers.background import BackgroundScheduler
import time
from src.jobs import daily_update

# 스케줄러 설정
scheduler = BackgroundScheduler()

# 매일 특정 시간에 작업 예약 (예: 매일 오전 9시에 실행)
# scheduler.add_job(my_scheduled_job, 'cron', hour=9, minute=0)
feed_url = "https://www.mk.co.kr/rss/50300009/"

scheduler.add_job(daily_update, 'cron', minute="*", args = [feed_url,])

if __name__ == '__main__':
    # 스케줄러 시작
    scheduler.start()
    # 메인 스레드가 종료되지 않도록 유지
    try:
        while True:
            time.sleep(60 * 120)  # 2초 간격으로 계속 체크
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()  # 종료 시 스케줄러도 중단
