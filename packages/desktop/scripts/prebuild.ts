#!/usr/bin/env bun
import { $ } from "bun"

import { downloadCliToResources, resolveChannel } from "./utils"

process.env.OPENCODE_VERSION = process.env.OPENCODE_VERSION || "1.18.34"
process.env.OPENCODE_CHANNEL = process.env.OPENCODE_CHANNEL || "latest"

const channel = resolveChannel()
await $`bun ./scripts/copy-icons.ts ${channel}`
await $`bun ./scripts/copy-metainfo.ts ${channel}`

await $`cd ../opencode && bun script/build-node.ts`
if (channel === "dev") await downloadCliToResources()
