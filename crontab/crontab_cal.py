import time

from apscheduler.schedulers.background import BackgroundScheduler

from application.app_context import calculator_id_demand_map


def my_job():
    crontab_list=calculator_id_demand_map
    for key, value in crontab_list.items():
        print(key, value)

def start_crontab():
    # 创建一个后台调度器
    scheduler = BackgroundScheduler()

    # 添加一个任务，使用interval触发器，每隔一小时执行一次my_job函数
    scheduler.add_job(my_job, 'interval', hours=1)

    # 开始调度器
    scheduler.start()

    # 这里可以添加你的主程序逻辑，调度器会在后台运行
    try:
        # 这里保持主程序运行，例如通过阻塞或者其它长时间运行的任务
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # 如果主程序被中断（如Ctrl+C），则关闭调度器
        scheduler.shutdown()