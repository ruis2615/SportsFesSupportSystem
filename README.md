# システムについて

このシステムは、2023年6月に実施した体育祭で開発・試験導入したシステムのソースコードです。

## データベース設計

### `users`テーブル
アカウントに関連する情報を保存しています。

| カラム名              | データ型        | `NULL`設定 | 内部値                                                             |
|-------------------|-------------|--------|-----------------------------------------------------------------|
| `user_id`         | `SERIAL4`   | 不可能    | 自動                                                              |
| `user_name`       | `TEXT`      | 不可能    | 自動(`YYYYMMDD-<user_id>`の形式)                                     |
| `user_password`   | `TEXT`      | 不可能    | 自動(ハッシュ値を保存)                                                    |
| `user_permission` | `TEXT`      | 不可能    | ・`all_permissions`：全権限<br/>・`only_my_team_entry`：自チームに関連するデータのみ |
| `user_type`       | `TEXT`      | 可能     | ・`0`<br/>・`1`                                                   |
| `user_created_at` | `TIMESTAMP` | 不可能    | 自動                                                              |
| `user_updated_at` | `TIMESTAMP` | 可能     | 自動                                                              |

### `teams`テーブル
チームに関連する情報を保存しています。

| カラム名                  | データ型      | `NULL`設定 | 内部値                 |
|-----------------------|-----------|--------|---------------------|
| `team_id`             | `SERIAL4` | 不可能    | 自動                  |
| `team_name`           | `TEXT`    | 不可能    | ユーザーが指定             |
| `team_leader`         | `TEXT`    | 可能     | ユーザーが指定             |
| `team_sub_leader`     | `TEXT`    | 可能     | ユーザーが指定             |
| `team_login_id`       | `TEXT`    | 不可能    | 自動的に`users`と紐づけ     |
| `team_login_password` | `TEXT`    | 不可能    | 自動的に`users`と紐づけ(平文) |

### `schedules`テーブル
スケジュールに関連する情報を保存しています。

| カラム名                  | データ型      | `NULL`設定 | 内部値         |
|-----------------------|-----------|----------|-------------|
| `schedule_id`         | `SERIAL4` | 不可能      | 自動          |
| `schedule_number`     | `INTEGER` | 不可能      | ユーザーが指定     |
| `schedule_name`       | `TEXT`    | 不可能      | ユーザーが指定     |
| `schedule_type`       | `INTEGER` | 不可能      | 自動(ユーザーが指定) |
| `schedule_option`     | `JSONB`   | 可能       | 自動(ユーザーが指定) |
| `schedule_started_at` | `TIME`    | 不可能      | 自動(ユーザーが指定) |
| `schedule_ended_at`    | `TIME`    | 不可能      | 自動(ユーザーが指定) |


### `scores`テーブル
得点に関連する情報を保存しています。

| カラム名               | データ型        | `NULL`設定 | 内部値     |
|--------------------|-------------|----------|---------|
| `score_id`         | `SERIAL4`   | 不可能      | 自動      |
| `schedule_id`      | `INTEGER`   | 不可能      | 自動      |
| `team_id`          | `INTEGER`   | 不可能      | 自動      |
| `race_number`      | `INTEGER`   | 不可能      | 自動      |
| `race_gender`      | `INTEGER`   | 不可能      | 自動      |
| `score`            | `INTEGER`   | 不可能      | ユーザーが指定 |
| `score_created_at` | `TIMESTAMP` | 不可能      | 自動      |
| `score_updated_at`  | `TIMESTAMP` | 可能       | 自動      |

### `entrys`テーブル
エントリーに関連する情報を保存しています。

| カラム名              | データ型        | `NULL`設定 | 内部値         |
|-------------------|-------------|----------|-------------|
| `entry_id`        | `SERIAL4`   | 不可能      | 自動          |
| `team_id`         | `INTEGER`   | 不可能      | 自動          |
| `schedule_id`     | `INTEGER`   | 不可能      | 自動          |
| `entry`           | `JSONB`     | 不可能      | 自動(ユーザーが指定) |
| `entry_created_at` | `TIMESTAMP` | 可能       | 自動          |
| `entry_updated_at` | `TIMESTAMP`  | 可能       | 自動          |

### `list_of_name`テーブル
全校生徒の名簿を保存しています。

| カラム名     | データ型      | `NULL`設定 | 内部値        |
|----------|-----------|----------|------------|
| `id`     | `SERIAL4` | 不可能      | 自動         |
| `number` | `TEXT`    | 不可能      | ユーザーが指定    |
| `name`   | `TEXT`    | 不可能      | ユーザーが指定    |
| `gender` | `TEXT`    | 不可能      | ユーザーが指定    |
| `team_id` | `INTEGER`  | 不可能      | 自動(ユーザーが指定 |

### `absence_report`テーブル
当日の欠席者情報を保存しています。

| カラム名         | データ型      | `NULL`設定 | 内部値         |
|--------------|-----------|----------|-------------|
| `absence_id` | `SERIAL4` | 不可能      | 自動          |
| `primary_id`  | `INTEGER`  | 不可能      | 自動(ユーザーが指定) |

### `options`テーブル
システムの設定に関連する情報を保存しています。

| カラム名          | データ型   | `NULL`設定 | 内部値                 |
|---------------|--------|----------|---------------------|
| `option_name` | `TEXT` | 不可能      | `master_option`(自動) |
| `option_value` | `JSONB` | 不可能      | 自動                  |

