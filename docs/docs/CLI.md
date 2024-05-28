# `sms`

CLI interface for the sms service simulator.

**Usage**:

```console
$ sms [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `-v, --version`: Print the current version.
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `generate`: Generate N SMS messages and add them to...
* `monitor`: Monitor SMS progress.
* `spawn-senders`: Send SMS messages.
* `tui`: Run the Terminal User Interface

## `sms generate`

Generate N SMS messages and add them to the queue.

**Usage**:

```console
$ sms generate [OPTIONS] [N]
```

**Arguments**:

* `[N]`: Number of sms messages to generate.  [default: 1000]

**Options**:

* `--target-dir TEXT`: Directory to write messages.  [default: inbox]
* `--help`: Show this message and exit.

## `sms monitor`

Monitor SMS progress.

**Usage**:

```console
$ sms monitor [OPTIONS] [TARGET_DIR]
```

**Arguments**:

* `[TARGET_DIR]`: directory to watch for sms results  [default: outbox]

**Options**:

* `--interval FLOAT`: Refresh Metrics Interval in seconds.  [default: 1.0]
* `--help`: Show this message and exit.

## `sms spawn-senders`

Send SMS messages.

**Usage**:

```console
$ sms spawn-senders [OPTIONS] [DEST_DIR]
```

**Arguments**:

* `[DEST_DIR]`: directory to write success/failre messages  [default: outbox]

**Options**:

* `--num-workers INTEGER`: Number of workers to send messages.  [default: 9]
* `--latency-mean INTEGER`: Mean latency in milliseconds.  [default: 50]
* `--failure-rate FLOAT`: Rate of failure in sending messages.  [default: 0.1]
* `--help`: Show this message and exit.

## `sms tui`

Run the Terminal User Interface

**Usage**:

```console
$ sms tui [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

