"""
Scheduler - Run agent at scheduled intervals
"""
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import pytz
import config
from agent import NSEPredictionAgent

logger = logging.getLogger(__name__)

class AgentScheduler:
    """Schedule agent to run at specific times"""
    
    def __init__(self):
        # IST timezone
        self.tz = pytz.timezone('Asia/Kolkata')
        self.scheduler = BackgroundScheduler(timezone=self.tz)
        self.agent = NSEPredictionAgent()
    
    def schedule_daily_analysis(self):
        """
        Schedule analysis at market close (3:30 PM IST)
        This analyzes the previous day's data at the end of trading day
        """
        try:
            # Run at 3:30 PM IST, Monday to Friday
            self.scheduler.add_job(
                func=self._run_analysis,
                trigger=CronTrigger(
                    hour=15,
                    minute=30,
                    day_of_week='mon-fri',
                    timezone=self.tz
                ),
                id='daily_analysis',
                name='Daily Market Analysis',
                replace_existing=True
            )
            logger.info("Scheduled daily analysis at 15:30 IST (Market Close)")
            
        except Exception as e:
            logger.error(f"Error scheduling daily analysis: {str(e)}")
    
    def schedule_weekly_training(self):
        """
        Schedule model retraining every Sunday
        """
        try:
            self.scheduler.add_job(
                func=self._run_training,
                trigger=CronTrigger(
                    day_of_week='sun',
                    hour=18,
                    minute=0,
                    timezone=self.tz
                ),
                id='weekly_training',
                name='Weekly Model Training',
                replace_existing=True
            )
            logger.info("Scheduled weekly training on Sundays at 18:00 IST")
            
        except Exception as e:
            logger.error(f"Error scheduling weekly training: {str(e)}")
    
    def schedule_full_pipeline(self):
        """Schedule both training and prediction"""
        self.schedule_weekly_training()
        self.schedule_daily_analysis()
    
    def start(self):
        """Start the scheduler"""
        try:
            if not self.scheduler.running:
                self.scheduler.start()
                logger.info("Scheduler started")
        except Exception as e:
            logger.error(f"Error starting scheduler: {str(e)}")
    
    def stop(self):
        """Stop the scheduler"""
        try:
            if self.scheduler.running:
                self.scheduler.shutdown()
                logger.info("Scheduler stopped")
        except Exception as e:
            logger.error(f"Error stopping scheduler: {str(e)}")
    
    def _run_analysis(self):
        """Run analysis task"""
        try:
            logger.info(f"[{datetime.now()}] Running scheduled analysis...")
            self.agent.analyze_and_predict()
        except Exception as e:
            logger.error(f"Error in scheduled analysis: {str(e)}")
    
    def _run_training(self):
        """Run training task"""
        try:
            logger.info(f"[{datetime.now()}] Running scheduled training...")
            self.agent.train_models()
        except Exception as e:
            logger.error(f"Error in scheduled training: {str(e)}")


def run_scheduler():
    """Start the scheduler"""
    scheduler = AgentScheduler()
    scheduler.schedule_full_pipeline()
    scheduler.start()
    
    try:
        logger.info("Scheduler is running. Press Ctrl+C to stop.")
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutting down scheduler...")
        scheduler.stop()


if __name__ == "__main__":
    run_scheduler()
