document.addEventListener('DOMContentLoaded', () => {
  // File contents dictionary for the interactive IDE
  const files = {
    'agent.ts': `import { LLM } from "@kritiai/core/llm";
import { ToolRegistry } from "@kritiai/core/tools";
import { SessionRunner } from "@kritiai/core/session";

export class KritiAgent {
  private runner: SessionRunner;

  constructor(private config: AgentConfig) {
    this.runner = new SessionRunner({
      model: config.model ?? "gemini-2.5-pro",
      temperature: 0.2,
      tools: ToolRegistry.getEnabledTools(),
    });
  }

  async runStep(instruction: string) {
    console.log("[KritiAI] Orchestrating autonomous turn...");
    const stream = await this.runner.stream({
      prompt: instruction,
      autonomousRepair: true,
    });
    return stream;
  }
}`,
    'tools.ts': `import { Tool } from "@kritiai/protocol";
import { execCommand, readFile, writeFile } from "@kritiai/system";

export const CoreTools: Tool[] = [
  {
    name: "edit_file",
    description: "Perform surgical code modifications with AST integrity",
    handler: async (args) => writeFile(args.path, args.content),
  },
  {
    name: "run_terminal",
    description: "Execute bash or PowerShell commands in isolated sandbox",
    handler: async (args) => execCommand(args.command),
  },
  {
    name: "code_intel_lsp",
    description: "Query TypeScript, Rust, Python, Go language servers",
    handler: async (args) => getLanguageDiagnostics(args.symbol),
  },
];`,
    'index.ts': `import { KritiAgent } from "./agent";
import { CoreTools } from "./tools";

async function main() {
  console.log("⚡ Welcome to KritiAI Studio v1.0.0");
  const agent = new KritiAgent({
    model: "claude-3-7-sonnet",
    workspace: process.cwd(),
  });

  const session = await agent.runStep("Implement full-stack payment webhook");
  for await (const chunk of session) {
    process.stdout.write(chunk.delta);
  }
}

main().catch(console.error);`,
    'package.json': `{
  "name": "my-kritiai-project",
  "version": "1.0.0",
  "type": "module",
  "dependencies": {
    "@kritiai/core": "^1.0.0",
    "@kritiai/sdk": "^1.0.0",
    "effect": "^3.12.0"
  },
  "scripts": {
    "start": "kritiai run src/index.ts"
  }
}`
  };

  // Syntax highlighter helper
  function highlightCode(code) {
    return code.split('\n').map((line, idx) => {
      let escaped = line
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');

      // Basic tokens
      escaped = escaped.replace(/(import|export|class|const|let|async|await|function|return|private|constructor|from|type)/g, '<span class="kw">$1</span>');
      escaped = escaped.replace(/(console|SessionRunner|ToolRegistry|KritiAgent|CoreTools|LLM)/g, '<span class="typ">$1</span>');
      escaped = escaped.replace(/(".*?"|'.*?'|`.*?`)/g, '<span class="str">$1</span>');
      escaped = escaped.replace(/(\/\/.*$)/g, '<span class="cm">$1</span>');

      return `<div class="code-line"><span class="line-num">${idx + 1}</span><span class="code-text">${escaped}</span></div>`;
    }).join('');
  }

  // File click handler
  const fileItems = document.querySelectorAll('.file-item');
  const activeTab = document.querySelector('.tab.active');
  const editorContent = document.getElementById('editor-content');

  function selectFile(filename) {
    fileItems.forEach(item => {
      item.classList.toggle('active', item.dataset.file === filename);
    });
    if (activeTab) {
      activeTab.textContent = filename;
    }
    if (editorContent && files[filename]) {
      editorContent.innerHTML = highlightCode(files[filename]);
    }
  }

  fileItems.forEach(item => {
    item.addEventListener('click', () => {
      selectFile(item.dataset.file);
    });
  });

  // Initial render
  selectFile('agent.ts');

  // Interactive Chat Assistant
  const chatMessages = document.getElementById('chat-messages');
  const chatInput = document.getElementById('chat-input');
  const chatSendBtn = document.getElementById('chat-send');

  const cannedResponses = {
    default: "I've analyzed your project workspace. All 4 files are indexed and LSP symbols are mapped. What would you like to build or modify?",
    bug: "Scanning workspace for potential issues... Found 0 type errors. Adding test harness for edge conditions in `agent.ts` now.",
    api: "Creating endpoint in `src/agent.ts` with streaming response support. Verification test passed successfully! 🚀",
    perf: "Optimized session runner loop! Reduced token overhead by 34% and enabled local KV model caching."
  };

  function sendChatMessage() {
    const text = chatInput.value.trim();
    if (!text) return;

    // User message
    const userMsg = document.createElement('div');
    userMsg.className = 'chat-msg msg-user';
    userMsg.innerHTML = `<div class="msg-tag">You</div><div>${text}</div>`;
    chatMessages.appendChild(userMsg);
    chatInput.value = '';

    // Scroll
    chatMessages.scrollTop = chatMessages.scrollHeight;

    // AI Response simulation
    setTimeout(() => {
      const lower = text.toLowerCase();
      let reply = cannedResponses.default;
      if (lower.includes('bug') || lower.includes('fix') || lower.includes('error')) {
        reply = cannedResponses.bug;
      } else if (lower.includes('api') || lower.includes('create') || lower.includes('build')) {
        reply = cannedResponses.api;
      } else if (lower.includes('speed') || lower.includes('fast') || lower.includes('perf')) {
        reply = cannedResponses.perf;
      }

      const aiMsg = document.createElement('div');
      aiMsg.className = 'chat-msg msg-ai';
      aiMsg.innerHTML = `<div class="msg-tag">KritiAI Agent</div><div>${reply}</div>`;
      chatMessages.appendChild(aiMsg);
      chatMessages.scrollTop = chatMessages.scrollHeight;
    }, 600);
  }

  if (chatSendBtn && chatInput) {
    chatSendBtn.addEventListener('click', sendChatMessage);
    chatInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') sendChatMessage();
    });
  }

  // Copy buttons
  document.querySelectorAll('.copy-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const code = btn.previousElementSibling?.textContent || btn.dataset.code;
      if (code) {
        navigator.clipboard.writeText(code.trim());
        const originalText = btn.textContent;
        btn.textContent = 'Copied!';
        setTimeout(() => {
          btn.textContent = originalText;
        }, 1500);
      }
    });
  });
});
