import sentry_sdk
from common.config import getConfig, common_config, getMode
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.threading import ThreadingIntegration

def InitSentry():
    sentryConfig: dict = common_config.get("sentry", {})
    sentry_sdk.init(
        dsn=sentryConfig.get("dsn", ""),
        debug=common_config.get("ultraDebug", False),
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
        release=common_config.get("version", "0.0.0"),
        environment=getMode(),
        integrations=[LoggingIntegration(), ThreadingIntegration()]
    )

