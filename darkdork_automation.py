#!/usr/bin/env python3
"""
DarkDork Automation Framework
Scheduled searches, continuous monitoring, and automated workflows
"""

import json
import time
import threading
from datetime import datetime, timedelta
from typing import List, Dict, Callable, Optional
import os


class ScheduledTask:
    """Represents a scheduled task"""

    def __init__(self, name: str, dork_query: str, target_domain: str = None,
                 schedule: str = "daily", enabled: bool = True,
                 callback: Callable = None):
        self.name = name
        self.dork_query = dork_query
        self.target_domain = target_domain
        self.schedule = schedule  # daily, weekly, hourly, custom
        self.enabled = enabled
        self.callback = callback
        self.last_run = None
        self.next_run = None
        self.run_count = 0

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'name': self.name,
            'dork_query': self.dork_query,
            'target_domain': self.target_domain,
            'schedule': self.schedule,
            'enabled': self.enabled,
            'last_run': self.last_run.isoformat() if self.last_run else None,
            'next_run': self.next_run.isoformat() if self.next_run else None,
            'run_count': self.run_count
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'ScheduledTask':
        """Create from dictionary"""
        task = cls(
            data['name'],
            data['dork_query'],
            data.get('target_domain'),
            data.get('schedule', 'daily'),
            data.get('enabled', True)
        )

        if data.get('last_run'):
            task.last_run = datetime.fromisoformat(data['last_run'])

        if data.get('next_run'):
            task.next_run = datetime.fromisoformat(data['next_run'])

        task.run_count = data.get('run_count', 0)

        return task


class TaskScheduler:
    """Schedule and execute tasks"""

    def __init__(self, tasks_file: str = "scheduled_tasks.json"):
        self.tasks_file = tasks_file
        self.tasks: List[ScheduledTask] = []
        self.running = False
        self.thread = None
        self.load_tasks()

    def load_tasks(self):
        """Load tasks from file"""
        if os.path.exists(self.tasks_file):
            try:
                with open(self.tasks_file, 'r') as f:
                    data = json.load(f)
                    self.tasks = [ScheduledTask.from_dict(t) for t in data]
            except Exception as e:
                print(f"Error loading tasks: {e}")

    def save_tasks(self):
        """Save tasks to file"""
        try:
            with open(self.tasks_file, 'w') as f:
                json.dump([t.to_dict() for t in self.tasks], f, indent=2)
        except Exception as e:
            print(f"Error saving tasks: {e}")

    def add_task(self, task: ScheduledTask):
        """Add a new task"""
        task.next_run = self._calculate_next_run(task)
        self.tasks.append(task)
        self.save_tasks()

    def remove_task(self, task_name: str) -> bool:
        """Remove a task by name"""
        original_count = len(self.tasks)
        self.tasks = [t for t in self.tasks if t.name != task_name]

        if len(self.tasks) < original_count:
            self.save_tasks()
            return True
        return False

    def enable_task(self, task_name: str):
        """Enable a task"""
        for task in self.tasks:
            if task.name == task_name:
                task.enabled = True
                task.next_run = self._calculate_next_run(task)
                self.save_tasks()
                break

    def disable_task(self, task_name: str):
        """Disable a task"""
        for task in self.tasks:
            if task.name == task_name:
                task.enabled = False
                self.save_tasks()
                break

    def _calculate_next_run(self, task: ScheduledTask) -> datetime:
        """Calculate next run time for task"""
        now = datetime.now()

        if task.schedule == 'hourly':
            return now + timedelta(hours=1)
        elif task.schedule == 'daily':
            return now + timedelta(days=1)
        elif task.schedule == 'weekly':
            return now + timedelta(weeks=1)
        elif task.schedule == 'monthly':
            return now + timedelta(days=30)
        elif task.schedule.startswith('every_'):
            # e.g., "every_2h", "every_30m"
            if 'h' in task.schedule:
                hours = int(task.schedule.split('_')[1].replace('h', ''))
                return now + timedelta(hours=hours)
            elif 'm' in task.schedule:
                minutes = int(task.schedule.split('_')[1].replace('m', ''))
                return now + timedelta(minutes=minutes)

        return now + timedelta(days=1)  # Default to daily

    def _execute_task(self, task: ScheduledTask):
        """Execute a task"""
        print(f"[{datetime.now().isoformat()}] Executing task: {task.name}")

        try:
            # Execute the dork query
            # This would integrate with the main DarkDork system
            if task.callback:
                task.callback(task.dork_query, task.target_domain)
            else:
                print(f"  Query: {task.dork_query}")
                if task.target_domain:
                    print(f"  Target: {task.target_domain}")

            task.last_run = datetime.now()
            task.run_count += 1
            task.next_run = self._calculate_next_run(task)

            print(f"  Next run: {task.next_run.isoformat()}")

        except Exception as e:
            print(f"  Error executing task: {e}")

        self.save_tasks()

    def run(self):
        """Start the scheduler"""
        self.running = True
        self.thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        self.thread.start()
        print("Task scheduler started")

    def stop(self):
        """Stop the scheduler"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        print("Task scheduler stopped")

    def _scheduler_loop(self):
        """Main scheduler loop"""
        while self.running:
            now = datetime.now()

            for task in self.tasks:
                if not task.enabled:
                    continue

                if task.next_run is None:
                    task.next_run = self._calculate_next_run(task)

                if now >= task.next_run:
                    self._execute_task(task)

            # Check every 30 seconds
            time.sleep(30)

    def list_tasks(self) -> List[Dict]:
        """List all tasks"""
        return [t.to_dict() for t in self.tasks]


class ContinuousMonitor:
    """Continuously monitor for changes"""

    def __init__(self):
        self.monitoring = False
        self.monitors = []

    def add_monitor(self, name: str, dork_query: str,
                   target_domain: str = None, check_interval: int = 3600):
        """Add a continuous monitor"""
        monitor = {
            'name': name,
            'dork_query': dork_query,
            'target_domain': target_domain,
            'check_interval': check_interval,
            'last_check': None,
            'last_results': None
        }
        self.monitors.append(monitor)

    def check_for_changes(self, monitor: Dict) -> Dict:
        """Check if results have changed"""
        # This would perform the actual search and compare results
        # For now, return mock data
        return {
            'changed': False,
            'new_results': 0,
            'removed_results': 0
        }

    def start_monitoring(self):
        """Start continuous monitoring"""
        self.monitoring = True
        print("Continuous monitoring started")

        # In a real implementation, this would run in background threads
        # and trigger alerts when changes are detected

    def stop_monitoring(self):
        """Stop continuous monitoring"""
        self.monitoring = False
        print("Continuous monitoring stopped")


class WorkflowEngine:
    """Execute automated workflows"""

    def __init__(self):
        self.workflows = []

    def create_workflow(self, name: str, steps: List[Dict]) -> str:
        """Create a new workflow"""
        workflow = {
            'id': len(self.workflows) + 1,
            'name': name,
            'steps': steps,
            'created': datetime.now().isoformat()
        }
        self.workflows.append(workflow)
        return workflow['id']

    def execute_workflow(self, workflow_id: int, context: Dict = None):
        """Execute a workflow"""
        workflow = next((w for w in self.workflows if w['id'] == workflow_id), None)

        if not workflow:
            print(f"Workflow {workflow_id} not found")
            return

        print(f"\nExecuting workflow: {workflow['name']}")
        print(f"Steps: {len(workflow['steps'])}\n")

        results = []

        for i, step in enumerate(workflow['steps'], 1):
            print(f"[Step {i}/{len(workflow['steps'])}] {step['name']}")

            try:
                result = self._execute_step(step, context)
                results.append(result)
                print(f"  Status: {'✓ Success' if result.get('success') else '✗ Failed'}")

                # Stop on failure if step is critical
                if not result.get('success') and step.get('critical', False):
                    print("  Critical step failed, stopping workflow")
                    break

            except Exception as e:
                print(f"  Error: {e}")
                if step.get('critical', False):
                    break

        print(f"\nWorkflow completed: {len([r for r in results if r.get('success')])} successful steps")

        return results

    def _execute_step(self, step: Dict, context: Dict = None) -> Dict:
        """Execute a workflow step"""
        step_type = step.get('type')

        if step_type == 'execute_dork':
            # Execute a dork query
            return {'success': True, 'type': 'execute_dork'}

        elif step_type == 'filter_results':
            # Filter results based on criteria
            return {'success': True, 'type': 'filter_results'}

        elif step_type == 'export':
            # Export results
            return {'success': True, 'type': 'export'}

        elif step_type == 'notify':
            # Send notification
            return {'success': True, 'type': 'notify'}

        elif step_type == 'integrate':
            # Call external integration
            return {'success': True, 'type': 'integrate'}

        else:
            return {'success': False, 'error': f'Unknown step type: {step_type}'}


class AutomationManager:
    """Manage all automation components"""

    def __init__(self):
        self.scheduler = TaskScheduler()
        self.monitor = ContinuousMonitor()
        self.workflow_engine = WorkflowEngine()

    def create_security_assessment_workflow(self, target_domain: str) -> int:
        """Create a complete security assessment workflow"""
        steps = [
            {
                'name': 'Search for exposed documents',
                'type': 'execute_dork',
                'params': {
                    'category': 'Exposed Documents',
                    'target': target_domain
                },
                'critical': False
            },
            {
                'name': 'Search for login pages',
                'type': 'execute_dork',
                'params': {
                    'category': 'Login Pages',
                    'target': target_domain
                },
                'critical': False
            },
            {
                'name': 'Search for configuration files',
                'type': 'execute_dork',
                'params': {
                    'category': 'Configuration',
                    'target': target_domain
                },
                'critical': False
            },
            {
                'name': 'Filter high-severity results',
                'type': 'filter_results',
                'params': {
                    'severity': ['Critical', 'High']
                },
                'critical': False
            },
            {
                'name': 'Export findings',
                'type': 'export',
                'params': {
                    'format': 'json',
                    'filename': f'assessment_{target_domain}_{datetime.now().strftime("%Y%m%d")}.json'
                },
                'critical': True
            },
            {
                'name': 'Send notification',
                'type': 'notify',
                'params': {
                    'message': f'Security assessment completed for {target_domain}',
                    'severity': 'info'
                },
                'critical': False
            }
        ]

        return self.workflow_engine.create_workflow(
            f"Security Assessment - {target_domain}",
            steps
        )

    def setup_daily_monitoring(self, target_domain: str, dorks: List[str]):
        """Setup daily monitoring for a target"""
        for dork in dorks:
            task = ScheduledTask(
                name=f"Daily {dork[:30]}... on {target_domain}",
                dork_query=dork,
                target_domain=target_domain,
                schedule='daily',
                enabled=True
            )
            self.scheduler.add_task(task)

        print(f"Setup {len(dorks)} daily monitoring tasks for {target_domain}")


def example_automation():
    """Example automation usage"""

    print("DarkDork Automation Framework")
    print("="*50)

    # Create automation manager
    manager = AutomationManager()

    # Create a security assessment workflow
    print("\n1. Creating security assessment workflow...")
    workflow_id = manager.create_security_assessment_workflow("example.com")
    print(f"   Created workflow ID: {workflow_id}")

    # Setup scheduled tasks
    print("\n2. Setting up scheduled tasks...")
    task = ScheduledTask(
        name="Daily Exposed Documents Check",
        dork_query="filetype:pdf confidential",
        target_domain="example.com",
        schedule="daily"
    )
    manager.scheduler.add_task(task)
    print("   Added daily task")

    # List all tasks
    print("\n3. Current scheduled tasks:")
    for task_dict in manager.scheduler.list_tasks():
        print(f"   - {task_dict['name']} ({task_dict['schedule']})")

    # Execute workflow
    print("\n4. Executing workflow...")
    # manager.workflow_engine.execute_workflow(workflow_id)

    print("\n✓ Automation setup complete!")


if __name__ == '__main__':
    example_automation()
