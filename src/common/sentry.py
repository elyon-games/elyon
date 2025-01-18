import sentry_sdk

def InitSentry():
    sentry_sdk.init(
        dsn="https://99aefb6971991a747cee9caf6a5fdeaf@o4508610774958080.ingest.de.sentry.io/4508610805629008",
        traces_sample_rate=1.0
    )

