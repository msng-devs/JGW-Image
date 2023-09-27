import os
from logging import getLogger

from src.core.config import Config
from src.helper.path import get_absolute_path
from src.crud.image_crud import find_all_by_converted_names
from src.db.database import get_db
from src.helper.mailstorm import send_mail

config = Config()
log = getLogger(__name__)


def clear_not_exist_img_task():
    log.info("[Scheduler] > Start Clear not exist image.")
    try:
        total_delete_count = clear_not_exist_img()
        send_mail("[Image] 작업 스케줄러 완료.", f"이미지 서버에서 {total_delete_count}개의 파일을 삭제했습니다.")
    except Exception as e:
        send_mail("[Image] 작업 스케줄러 오류.", f"이미지 서버에서 작업 스케줄러를 실행하는 중 오류가 발생했습니다.\n{str(e)}")


def clear_not_exist_img():
    total_delete_count = 0
    path = get_absolute_path([config.FILE_PATH, "image"])
    names = []

    for files in os.scandir(path):
        if files.is_file():
            names.append(files.name)

        if len(names) >= 1000:
            total_delete_count += clear(names)
            names.clear()

    if len(names) > 0:
        total_delete_count += clear(names)

    return total_delete_count


def clear(files: list):
    cnt = 0

    with get_db() as db:
        targets = find_all_by_converted_names(db, files)

    if len(targets) == len(files):
        return 0

    for target in targets:
        if target.IMAGE_META_CONVERTED_NM in files:
            files.remove(target.IMAGE_META_CONVERTED_NM)

    for file in files:
        path = get_absolute_path([config.FILE_PATH, "image", file])
        if os.path.exists(path):
            os.remove(path)
            cnt += 1
        else:
            log.warning(f"[Scheduler] > File not exist: {path}")
