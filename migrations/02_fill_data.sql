--
-- Up
--

SET FOREIGN_KEY_CHECKS = 0;
START TRANSACTION;
-- ----------------------------
-- Records of problem
-- ----------------------------
INSERT INTO `problem` (problem_id, description)
VALUES
    (1, 'No such file or directory'),
    (2, 'Permission denied'),
    (3, 'command not found'),
    (4, 'user sit is currently used by process'),
    (5, 'Operation not permitted'),
    (6, 'Cannot get exclusive access to /dev/md0:Perhaps a running process, mounted filesystem or active volume group?'),
    (7, 'Can''t initialize physical volume'),
    (8, 'not mounted'),
    (9, 'special device /dev/mapper/truecrypt1 does not exist'),
    (10, 'Unable to locate package'),
    (11, 'Unrecognized md component device'),
    (12, 'Couldn''t open for /dev/sdb for write - not zeroing'),
    (13, 'cp: missing destination file operand after'),
    (14, 'ln: failed to create hard link : File exists'),
    (15, 'Only root may remove a user or group from the system'),
    (16, 'Group not removed because it has other members'),
    (17, 'Unrecognized operand'),
    (18, 'mdadm: Device or resource busy'),
    (19, 'The following packages have unmet dependencies'),
    (20, 'iptables Unknown option "INPUT"'),
    (21, 'fdisk: bad usage'),
    (22, 'mount point does not exist'),
    (23, 'dd: failed to open: Not a directory'),
    (24, 'dd: failed to open: Is a directory'),
    (25, 'mkfs.ext: invalid blocks on device'),
    (26, 'sysctl: "net.ipv4.tcp_synack_retires" must be of the form name=value'),
    (27, 'iptables: host/network not found'),
    (28, 'iptables: multiple flags not allowed'),
    (29, 'Bad argument');

-- ----------------------------
-- Records of recommendation
-- ----------------------------
INSERT INTO `recommendation` (recommendation_id, recommendation)
VALUES
    (1, 'Проверьте правильность введенного названия папки/файла'),
    (2, 'Проверьте правильность введенного пути. Если путь относительный, проверьте его относительно текущей директории (используйте команду pwd, чтобы узнать ее)'),
    (3, 'Отредактируйте права на файл/папку с помощью команды chmod. Проверить права можно командой ls -l'),
    (4, 'Добавьте sudo в начало команды и попробуйте снова'),
    (5, 'Проверьте правильность введенной команды'),
    (6, 'Необходимо разлогинить удаляемого пользователя'),
    (7, 'Добавьте флаг -f к команде (это может быть опасно)'),
    (8, 'Завершите указанный процесс (с помощью команды kill -9 <pid>, где pid - номер процесса)'),
    (9, 'Отмонтируйте указанный диск с помощью команды umount'),
    (10, 'Проверьте, что работаете с нужным диском'),
    (11, 'Попробуйте следующие команды (они удалят таблицу разделов): ''sudo dd if=/dev/zero of=/dev/sd* bs=1k count=1'', ''sudo blockdev --rereadpt /dev/sd*'''),
    (12, 'Примонтируйте диск с помошью команды mount'),
    (13, 'Попробуйте команду (вместо mount) sudo truecrypt -k <путь к файлу-ключу> /dev/sd* <точка монтирования>'),
    (14, 'Проверьте название пакета (серьезно)'),
    (15, 'Обновите кэш репозиториев: sudo apt update'),
    (16, 'Проверьте, доступен ли пакет для вашей версии дистрибутива (на сайте официальном дистрибутива, в разделе packages). Версию вашего дистрибутива можно узнать с помощью команды lsb_release -a'),
    (17, 'Если пакет доступен для вашей версии дистрибутива, добавьте репозиторий, в котором он находится: sudo add-apt-repository {название репозитория}; sudo apt update'),
    (18, 'Если пакета нет в репозиториях, его можно попробовать скомпилировать самостоятельно (если исходники открыты) или установить .deb пакетом (если его предварительно найти, конечно), скачав его с помощью wget, после чего распаковав с помощью dpkg'),
    (19, 'RAID не существует или разрушен или указанный диск не принаждлежит к нему. Попробуйте другой диск или проверьте состояние массива.'),
    (20, 'Укажите команде конечную папку/файл вторым аргументом'),
    (21, 'Перейдите в режим суперпользователя с помощью команды sudo su и попробуйте снова'),
    (22, 'Удалите других пользователей из группы с помощью команды gpasswd -d user group (или удалите других пользователей)'),
    (23, 'Посмотрите документацию по команде, добавив к ней флаг -h или параметр help. Можно также проверить через man {название утилиты}'),
    (24, 'Попробуйте остановить процесс (или разрушить RAID-массив), который использует данных файл/ресурс'),
    (25, 'Необходимо установить указанные пакеты (которых не хватает) указанных версий с помощью команды sudo apt install (если не совпадает версия, то существующие пакеты необходимо предварительно удалить)'),
    (26, 'Необходимо очистить репозитории (удалить "недоустановленные пакеты") с помощью команды sudo apt-get clean'),
    (27, 'Попробуйте удалить слэш в конце ошибочного пути, указанного в выводе'),
    (28, 'Попробуйте создать файловые системы на каждом диске по отдельности, а не разом, используя синтаксис [1-2]'),
    (29, 'Установите параметру значение (имя_параметра=значение)'),
    (30, 'Проверьте введенное название сети'),
    (31, 'Проверьте корректность параметров (например, перед параметром указан один дефис вместо двух)'),

-- ----------------------------
-- Records of problem_recommendation
-- ----------------------------
INSERT INTO `problem_recommendation`
VALUES
    (1, 1, 1),
    (1, 2, 2),
    (2, 3, 1),
    (2, 4, 2),
    (3, 5, 2),
    (4, 6, 3),
    (4, 7, 2),
    (4, 8, 1),
    (3, 4, 1),
    (5, 4, 2),
    (6, 9, 2),
    (6, 8, 1),
    (7, 10, 2),
    (7, 11, 1),
    (8, 12, 2),
    (9, 13, 2),
    (9, 1, 1),
    (10, 14, 5),
    (10, 15, 4),
    (10, 16, 3),
    (10, 17, 2),
    (10, 18, 1),
    (11, 19, 1),
    (12, 19, 1),
    (13, 20, 1),
    (14, 20, 3),
    (14, 1, 2),
    (14, 2, 1),
    (15, 4, 2),
    (15, 21, 1),
    (16, 22, 1),
    (17, 1, 3),
    (17, 2, 2),
    (17, 23, 1),
    (18, 24, 1),
    (19, 25, 2),
    (19, 26, 1),
    (20, 5, 2),
    (20, 23, 1),
    (21, 23, 1),
    (22, 10, 3),
    (22, 1, 2),
    (22, 2, 1),
    (23, 1, 2),
    (23, 2, 1),
    (24, 27, 3),
    (24, 1, 2),
    (24, 2, 1),
    (25, 28, 1),
    (26, 29, 1),
    (27, 30, 2),
    (27, 31, 1),
    (28, 31, 1),
    (29, 31, 1);

COMMIT;
SET FOREIGN_KEY_CHECKS = 1;
--
-- Down
--
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE `problem_recommendation`;
TRUNCATE TABLE `problem`;
TRUNCATE TABLE `recommendation`;
SET FOREIGN_KEY_CHECKS = 1;