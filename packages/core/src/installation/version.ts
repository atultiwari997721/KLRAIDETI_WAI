declare global {
  const OPENCODE_VERSION: string
  const OPENCODE_CHANNEL: string
}

const envVersion = typeof process !== "undefined" ? process.env?.OPENCODE_VERSION : undefined
const envChannel = typeof process !== "undefined" ? process.env?.OPENCODE_CHANNEL : undefined

export const InstallationVersion =
  typeof OPENCODE_VERSION === "string" && !OPENCODE_VERSION.startsWith("0.0.0") && OPENCODE_VERSION !== "local"
    ? OPENCODE_VERSION
    : (envVersion && !envVersion.startsWith("0.0.0") && envVersion !== "local" ? envVersion : "1.18.34")

export const InstallationChannel =
  typeof OPENCODE_CHANNEL === "string" && OPENCODE_CHANNEL !== "local" && OPENCODE_CHANNEL !== "dev"
    ? OPENCODE_CHANNEL
    : (envChannel && envChannel !== "dev" && envChannel !== "local" ? envChannel : "latest")

export const InstallationLocal = false

