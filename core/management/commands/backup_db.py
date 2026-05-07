import shutil
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Backup SQLite database"

    def handle(self, *args, **kwargs):
        db_path = settings.BASE_DIR / "db.sqlite3"
        backup_dir = settings.BASE_DIR / "backups"

        backup_dir.mkdir(exist_ok=True)

        if not db_path.exists():
            self.stdout.write(self.style.ERROR("Database file not found."))
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = backup_dir / f"db_backup_{timestamp}.sqlite3"

        shutil.copy2(db_path, backup_file)

        self.stdout.write(
            self.style.SUCCESS(f"Database backup created: {backup_file}")
        )