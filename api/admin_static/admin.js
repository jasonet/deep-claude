/* ================================================================
   I18N — English  Chinese
   ================================================================ */
const I18N = {
  /* ---- static HTML keys ---- */
  title:          ["Deep Claude Code Admin",  "Deep Claude Code 管理"],
  brand:          ["Deep Claude Code",        "Deep Claude Code"],
  brandSub:       ["Server Control",          "服务控制台"],
  eyebrow:        ["Local Admin",             "本地管理"],
  pageTitle:      ["Runtime Config",          "运行时配置"],
  providersTitle: ["Providers",               "服务商"],
  checkLocal:     ["Check local",             "检查本地"],
  genEnv:         ["Generated Env",           "生成的环境变量"],
  genEnvDesc:     ["Read-only preview of the managed config file.", "托管配置文件的只读预览。"],
  validate:       ["Validate",                "校验"],
  apply:          ["Apply",                   "应用"],

  /* ---- section labels ---- */
  sec_providers_l:  ["Provider Keys/API", "服务商 KEY/API"],
  sec_models_l:     ["Model Routing",  "模型路由"],
  sec_thinking_l:   ["Thinking",       "思考模式"],
  sec_runtime_l:    ["Runtime",        "运行时"],
  sec_messaging_l:  ["Messaging",      "消息通道"],
  sec_voice_l:      ["Voice",          "语音"],
  sec_web_tools_l:  ["Web Tools",      "网络工具"],
  sec_diagnostics_l:["Diagnostics",    "诊断"],
  sec_smoke_l:      ["Smoke Tests",    "冒烟测试"],

  /* ---- section descriptions ---- */
  sec_providers_d:  ["Provider keys, local endpoints, and proxy settings.", "服务商密钥、本地端点和代理设置。"],
  sec_models_d:     ["Provider-prefixed models used for Claude model tiers.", "Claude 模型层级使用的服务商前缀模型。"],
  sec_thinking_d:   ["Global and tier-specific thinking behavior.", "全局和层级特定的思考行为。"],
  sec_runtime_d:    ["Server API token, rate limits, timeouts, and process settings.", "服务端 API 令牌、速率限制、超时和进程设置。"],
  sec_messaging_d:  ["Discord, Telegram, CLI workspace, and session settings.", "Discord、Telegram、CLI 工作区和会话设置。"],
  sec_voice_d:      ["Voice note transcription settings.", "语音笔记转录设置。"],
  sec_web_tools_d:  ["Local Anthropic web_search and web_fetch behavior.", "本地 Anthropic 网页搜索和抓取行为。"],
  sec_diagnostics_d:["Logging and debugging flags.", "日志和调试标志。"],
  sec_smoke_d:      ["Optional live smoke-test model overrides.", "可选的实时冒烟测试模型覆盖。"],
  sec_tools_l:      ["Tools",          "工具推荐"],
  sec_tools_d:      ["Recommended companion tools for DeepSeek.", "DeepSeek 配套推荐工具。"],

  /* ---- status / pills ---- */
  loading:      ["Loading",          "加载中"],
  running:      ["Running",          "运行中"],
  error:        ["Error",            "错误"],
  configured:   ["Configured",       "已配置"],
  missingKey:   ["Missing key",      "缺少密钥"],
  missingUrl:   ["Missing URL",      "缺少网址"],
  unknown:      ["Not checked",      "未检查"],
  offline:      ["Offline",          "离线"],
  reachable:    ["Reachable",        "可连接"],

  /* ---- actions ---- */
  test:           ["Test",            "测试"],
  refreshModels:  ["Refresh models",  "刷新模型"],
  showAdvanced:   ["Show advanced",   "显示高级"],
  hideAdvanced:   ["Hide advanced",   "隐藏高级"],
  testing:        ["Testing",         "测试中"],
  noChanges:      ["No changes",      "无更改"],
  unsaved1:       [" unsaved change", " 处未保存更改"],
  unsavedN:       [" unsaved changes"," 处未保存更改"],

  /* ---- messages ---- */
  msgLoading:       ["Loading admin config",   "正在加载管理配置"],
  msgValid:         ["Config shape is valid",   "配置格式有效"],
  msgApplied:       ["Applied",                 "已应用"],
  msgAppliedRestart:["Applied. Restart dc-server to use: ","已应用。重启 dc-server 以使用："],
  msgRestarting:    ["Applied. Restarting server...", "已应用。正在重启服务端…"],

  /* ---- field sources ---- */
  src_default:         ["default",      "默认"],
  src_template:        ["template",     "模板"],
  src_repo_env:        ["repo .env",    "仓库 .env"],
  src_managed_env:     ["managed",      "托管"],
  src_explicit_env_file:["DCC_ENV_FILE","DCC_ENV_FILE"],
  src_process:         ["process env",  "进程环境"],
  locked:              [" locked",      " 已锁定"],
  inherit:             ["Inherit",      "继承"],
  enabled:             ["Enabled",      "启用"],
  disabled:            ["Disabled",     "禁用"],

  /* ---- provider names ---- */
  p_nvidia_nim:  ["NVIDIA NIM",  "NVIDIA NIM"],
  p_open_router: ["OpenRouter",  "OpenRouter"],
  p_deepseek:    ["DeepSeek",   "DeepSeek"],
  p_lmstudio:    ["LM Studio",  "LM Studio"],
  p_llamacpp:    ["llama.cpp",  "llama.cpp"],
  p_ollama:      ["Ollama",     "Ollama"],
  p_kimi:        ["Kimi",       "Kimi"],
  p_wafer:       ["Wafer",      "Wafer"],
  p_opencode:    ["OpenCode Zen","OpenCode Zen"],
  p_ninerouter:  ["9routor",    "9routor"],
  p_omlx:        ["oMLX",       "oMLX"],

  /* ---- misc dynamic ---- */
  modelsCount:   [" models",     " 个模型"],
  noModels:      ["No models returned", "没有返回模型"],
  noUrl:         ["No local URL configured", "未配置本地地址"],
  configuredPlaceholder: ["Configured - enter a new value to replace", "已配置 - 输入新值以替换"],
  notConfigured: ["Not configured", "未配置"],

  /* ---- model restore ---- */
  restoreDSv4:   ["Restore DS V4", "恢复 DS V4 默认"],
  dsRestored:    ["DeepSeek V4 defaults restored", "已恢复 DeepSeek V4 默认配置"],

  /* ---- CLI commands ---- */
  cliLabel:      ["CLI Commands", "客户端指令"],
  cliCopied:     ["Copied to clipboard", "已复制到剪贴板"],
  cliNoApiKey:   ["DeepSeek API Key not configured. Open anyway?", "DeepSeek API Key 未配置。确定继续打开终端？"],

  /* ---- language toggle ---- */
  langLabel:     ["EN", "中"],
};

let currentLang = (function(){
  try { return localStorage.getItem("fcc-admin-lang") || "en"; }
  catch(_) { return "en"; }
})();

function t(key) {
  const entry = I18N[key];
  if (!entry) return key;
  return currentLang === "zh" ? (entry[1] || entry[0]) : entry[0];
}

function applyStaticTranslations() {
  document.querySelectorAll("[data-i18n]").forEach(function(el) {
    var key = el.getAttribute("data-i18n");
    var trans = I18N[key];
    if (trans) {
      el.textContent = currentLang === "zh" ? trans[1] : trans[0];
    }
  });
  document.documentElement.lang = currentLang === "zh" ? "zh-CN" : "en";
}

function toggleLang() {
  currentLang = currentLang === "zh" ? "en" : "zh";
  try { localStorage.setItem("fcc-admin-lang", currentLang); } catch(_) {}
  applyStaticTranslations();
  load().catch(function(e) { showMessage(e.message, "error"); });
}

/* ================================================================
   SECTION ICONS & COLORS
   ================================================================ */
const SECTION_ICONS = {
  providers: "◈",
  models: "⊙",
  thinking: "◇",
  runtime: "⚙",
  messaging: "☰",
  voice: "♪",
  web_tools: "⌘",
  diagnostics: "⚑",
  smoke: "△",
  tools: "⬡",
};

const SECTION_COLORS = {
  providers:  "#59d994",
  models:     "#7cc7ff",
  thinking:   "#c4a7ff",
  runtime:    "#f5b74f",
  messaging:  "#56d4dd",
  voice:      "#ff7eb6",
  web_tools:  "#a3d944",
  diagnostics:"#ff746c",
  smoke:      "#aaa197",
  tools:      "#2fb984",
};

function sectionColor(sectionId) {
  return SECTION_COLORS[sectionId] || "#aaa197";
}

function sectionIconBg(color) {
  return color + "1a";
}

function sectionLabel(sectionId) {
  return t("sec_" + sectionId + "_l");
}

function sectionDesc(sectionId) {
  return t("sec_" + sectionId + "_d");
}

/* ================================================================
   STATE
   ================================================================ */
const state = {
  config: null,
  status: null,
  fields: new Map(),
  localStatus: new Map(),
  modelOptions: [],
};

const MASKED_SECRET = "********";

const byId = function(id) { return document.getElementById(id); };

function sourceLabel(source) {
  return t("src_" + source);
}

function providerIcon(providerId) {
  // LobeHub CDN icons for known providers
  var map = {
    deepseek: "https://unpkg.com/@lobehub/icons-static-svg@latest/icons/deepseek.svg",
    open_router: "https://unpkg.com/@lobehub/icons-static-svg@latest/icons/openrouter.svg",
    ollama: "https://unpkg.com/@lobehub/icons-static-svg@latest/icons/ollama.svg",
    nvidia_nim: "https://unpkg.com/@lobehub/icons-static-svg@latest/icons/nvidia.svg",
    kimi: "https://unpkg.com/@lobehub/icons-static-svg@latest/icons/moonshot.svg",
    lmstudio: "https://unpkg.com/@lobehub/icons-static-svg@latest/icons/lmstudio.svg",
    llamacpp: "https://unpkg.com/@lobehub/icons-static-svg@latest/icons/llamacpp.svg",
    wafer: "https://unpkg.com/@lobehub/icons-static-svg@latest/icons/wafer.svg",
    opencode: "https://unpkg.com/@lobehub/icons-static-svg@latest/icons/opencode.svg",
    ninerouter: "https://unpkg.com/@lobehub/icons-static-svg@latest/icons/openai.svg",
    omlx: "https://unpkg.com/@lobehub/icons-static-svg@latest/icons/apple.svg",
  };
  return map[providerId] || "";
}

function providerName(providerId) {
  var key = "p_" + providerId;
  var entry = I18N[key];
  if (entry) return currentLang === "zh" ? entry[1] : entry[0];
  return providerId
    .split("_")
    .map(function(part) { return part.charAt(0).toUpperCase() + part.slice(1); })
    .join(" ");
}

function statusClass(status) {
  if (["configured", "reachable", "running"].indexOf(status) >= 0) return "ok";
  if (["missing_key", "missing_url", "unknown"].indexOf(status) >= 0) return "warn";
  if (["offline", "error"].indexOf(status) >= 0) return "error";
  return "neutral";
}

function statusLabel(status) {
  return t(status) || status;
}

async function api(path, options) {
  options = options || {};
  var response = await fetch(path, {
    headers: Object.assign({ "Content-Type": "application/json" }, options.headers || {}),
    method: options.method,
    body: options.body,
  });
  if (!response.ok) {
    throw new Error(response.status + " " + response.statusText);
  }
  return response.json();
}

/* ================================================================
   LOAD
   ================================================================ */
async function load() {
  showMessage(t("msgLoading"));
  var results = await Promise.all([
    api("/admin/api/config"),
    api("/admin/api/status"),
  ]);
  state.config = results[0];
  state.status = results[1];
  state.fields = new Map(results[0].fields.map(function(f) { return [f.key, f]; }));
  updateHeader(results[1]);
  renderNav(results[0].sections);
  renderProviders(results[0].provider_status);
  renderSections(results[0].sections, results[0].fields);
  byId("configPath").textContent = results[0].paths.managed;
  await validate(false);
  await refreshLocalStatus();
  updateDirtyState();
  updateLangToggle();
  showMessage("");
}

function normalizeHost(host) {
  if (!host || host === "0.0.0.0" || host === "::") return "127.0.0.1";
  return host;
}

function updateHeader(status) {
  var pill = byId("serverStatus");
  pill.textContent = t("running");
  pill.className = "status-pill ok";
  byId("modelBadge").textContent = status.model || "";
  var host = normalizeHost(status.host);
  var port = status.port || 8082;
  byId("proxyUrl").textContent = "http://" + host + ":" + port;
  byId("adminUrl").textContent = "http://" + host + ":" + port + "/admin";
}

function updateLangToggle() {
  byId("langToggle").textContent = t("langLabel");
}

/* ================================================================
   NAV
   ================================================================ */
function renderNav(sections) {
  var nav = byId("sectionNav");
  nav.innerHTML = "";
  sections.forEach(function(section, index) {
    var clr = sectionColor(section.id);
    var button = document.createElement("button");
    button.type = "button";
    button.className = "nav-link" + (index === 0 ? " active" : "");
    button.style.color = clr;

    var icon = document.createElement("span");
    icon.className = "nav-icon";
    icon.textContent = SECTION_ICONS[section.id] || "●";
    icon.style.color = clr;
    icon.style.background = sectionIconBg(clr);

    var label = document.createElement("span");
    label.textContent = sectionLabel(section.id);

    button.appendChild(icon);
    button.appendChild(label);
    button.addEventListener("click", function() {
      document.querySelectorAll(".nav-link").forEach(function(l) { l.classList.remove("active"); });
      button.classList.add("active");
      byId("section-" + section.id).scrollIntoView({ behavior: "smooth" });
    });
    nav.appendChild(button);
  });
}

/* ================================================================
   PROVIDERS
   ================================================================ */
/* ---- Provider order persistence ---- */
function loadProviderOrder() {
  try {
    var raw = localStorage.getItem("fcc-provider-order");
    if (!raw) return null;
    var arr = JSON.parse(raw);
    // Dedup and validate
    if (!Array.isArray(arr)) return null;
    var seen = {}; var clean = [];
    for (var i = 0; i < arr.length; i++) {
      if (typeof arr[i] === "string" && !seen[arr[i]]) {
        seen[arr[i]] = true;
        clean.push(arr[i]);
      }
    }
    return clean;
  } catch(_) { return null; }
}
function saveProviderOrder(order) {
  try { localStorage.setItem("fcc-provider-order", JSON.stringify(order)); } catch(_) {}
}

function sortProviders(providerStatus) {
  var saved = loadProviderOrder();
  if (saved && saved.length) {
    var map = {};
    providerStatus.forEach(function(p) { map[p.provider_id] = p; });
    var sorted = [];
    var seen = {};
    saved.forEach(function(id) {
      if (map[id] && !seen[id]) { seen[id] = true; sorted.push(map[id]); }
    });
    // Append any new providers not in saved order
    providerStatus.forEach(function(p) {
      if (!seen[p.provider_id]) { seen[p.provider_id] = true; sorted.push(p); }
    });
    return sorted;
  }
  // Default: DeepSeek first
  return providerStatus.slice().sort(function(a, b) {
    if (a.provider_id === "deepseek") return -1;
    if (b.provider_id === "deepseek") return 1;
    return a.provider_id.localeCompare(b.provider_id);
  });
}

/* ---- Drag and drop ---- */
var dragSrc = null;

function handleDragStart(e) {
  dragSrc = this.closest(".provider-card");
  if (!dragSrc) return;
  dragSrc.classList.add("dragging");
  e.dataTransfer.effectAllowed = "move";
}

function handleDragOver(e) {
  e.preventDefault();
  e.dataTransfer.dropEffect = "move";
  return false;
}

function handleDrop(e) {
  e.preventDefault();
  e.stopPropagation();
  var target = this.closest(".provider-card");
  if (!dragSrc || !target || dragSrc === target) return;
  var grid = byId("providerGrid");
  var next = target.nextSibling;
  if (next === dragSrc) next = dragSrc.nextSibling;
  grid.insertBefore(dragSrc, next);
  persistProviderOrder();
}

function handleDragEnd() {
  if (dragSrc) dragSrc.classList.remove("dragging");
  dragSrc = null;
}

function persistProviderOrder() {
  var ids = [];
  var cards = byId("providerGrid").querySelectorAll(".provider-card");
  for (var i = 0; i < cards.length; i++) {
    ids.push(cards[i].dataset.provider);
  }
  saveProviderOrder(ids);
}

function renderProviders(providerStatus) {
  var grid = byId("providerGrid");
  grid.innerHTML = "";
  var sorted = sortProviders(providerStatus);
  sorted.forEach(function(provider) {
    var card = document.createElement("article");
    card.className = "provider-card";
    card.dataset.provider = provider.provider_id;
    card.draggable = true;
    card.addEventListener("dragstart", handleDragStart);
    card.addEventListener("dragover", handleDragOver);
    card.addEventListener("drop", handleDrop);
    card.addEventListener("dragend", handleDragEnd);

    // Drag handle
    var handle = document.createElement("span");
    handle.className = "drag-handle";
    handle.textContent = "⠿";
    card.appendChild(handle);

    // Provider icon from LobeHub CDN
    var iconUrl = providerIcon(provider.provider_id);
    var iconEl = document.createElement("img");
    iconEl.className = "provider-icon";
    iconEl.src = iconUrl;
    iconEl.alt = "";
    iconEl.onerror = function() { this.style.display = "none"; };

    var nameEl = document.createElement("strong");
    nameEl.textContent = providerName(provider.provider_id);

    var title = document.createElement("div");
    title.className = "provider-title";
    title.appendChild(iconEl);
    title.appendChild(nameEl);

    var pill = document.createElement("span");
    pill.className = "status-pill " + statusClass(provider.status);
    pill.textContent = statusLabel(provider.status);
    title.appendChild(pill);

    var meta = document.createElement("div");
    meta.className = "provider-meta";
    if (provider.kind === "local") {
      meta.textContent = provider.base_url || t("noUrl");
    } else {
      meta.textContent = provider.credential_env;
      if (provider.credential_url) {
        meta.appendChild(document.createElement("br"));
        var keyLink = document.createElement("a");
        keyLink.href = provider.credential_url;
        keyLink.target = "_blank";
        keyLink.rel = "noopener";
        keyLink.className = "provider-key-link";
        keyLink.textContent = "Get API Key →";
        meta.appendChild(keyLink);
      }
    }

    var button = document.createElement("button");
    button.type = "button";
    button.className = "test-button";
    button.textContent = provider.kind === "local" ? t("test") : t("refreshModels");
    button.addEventListener("click", function() { testProvider(provider.provider_id, button); });

    card.append(title, meta, button);
    grid.appendChild(card);
  });
}

function updateProviderCard(providerId, status, label, metaText) {
  var card = document.querySelector('[data-provider="' + providerId + '"]');
  if (!card) return;
  var pill = card.querySelector(".status-pill");
  pill.className = "status-pill " + statusClass(status);
  pill.textContent = label;
  if (metaText) {
    card.querySelector(".provider-meta").textContent = metaText;
  }
}

/* ================================================================
   SECTIONS
   ================================================================ */
function renderSections(sections, fields) {
  var container = byId("formSections");
  container.innerHTML = "";
  var bySection = new Map();
  sections.forEach(function(s) { bySection.set(s.id, []); });
  fields.forEach(function(f) {
    if (!bySection.has(f.section)) bySection.set(f.section, []);
    bySection.get(f.section).push(f);
  });

  sections.forEach(function(section) {
    var clr = sectionColor(section.id);
    var sectionEl = document.createElement("section");
    sectionEl.className = "settings-section";
    sectionEl.id = "section-" + section.id;

    var heading = document.createElement("div");
    heading.className = "section-heading";

    var left = document.createElement("div");
    left.className = "section-heading-left";

    var icon = document.createElement("span");
    icon.className = "section-icon";
    icon.textContent = SECTION_ICONS[section.id] || "●";
    icon.style.color = clr;
    icon.style.background = sectionIconBg(clr);

    var text = document.createElement("div");
    text.innerHTML = "<h3>" + sectionLabel(section.id) + "</h3><p>" + sectionDesc(section.id) + "</p>";
    text.querySelector("h3").style.color = clr;

    left.appendChild(icon);
    left.appendChild(text);

    // Right side: restore-btn (models only) + advanced toggle
    var right = document.createElement("div");
    right.className = "section-heading-right";

    if (section.id === "models") {
      var restoreBtn = document.createElement("button");
      restoreBtn.type = "button";
      restoreBtn.className = "ghost-button";
      restoreBtn.textContent = t("restoreDSv4");
      restoreBtn.title = "deepseek-chat / deepseek-reasoner";
      restoreBtn.addEventListener("click", function() {
        restoreDeepSeekDefaults();
      });
      right.appendChild(restoreBtn);
    }

    var sectionFields = bySection.get(section.id) || [];
    if (sectionFields.some(function(f) { return f.advanced; })) {
      var toggle = document.createElement("button");
      toggle.type = "button";
      toggle.className = "ghost-button";
      toggle.textContent = t("showAdvanced");
      toggle.addEventListener("click", function() {
        var showing = sectionEl.classList.toggle("show-advanced");
        toggle.textContent = showing ? t("hideAdvanced") : t("showAdvanced");
      });
      right.appendChild(toggle);
    }

    heading.appendChild(left);
    heading.appendChild(right);
    sectionEl.appendChild(heading);

    // Render content: tools section has cards, others have fields
    if (section.id === "tools") {
      renderTools(sectionEl, clr);
    } else {
      var grid = document.createElement("div");
      grid.className = "field-grid";
      (bySection.get(section.id) || []).forEach(function(field) {
        grid.appendChild(renderField(field, section.id));
      });
      sectionEl.appendChild(grid);
    }

    container.appendChild(sectionEl);
  });
}

/* ---- Tool cards ---- */
var TOOLS = [
  {
    name: "DeepSeek-TUI",
    url: "https://github.com/Hmbown/DeepSeek-TUI",
    desc: "Terminal UI client for DeepSeek API.",
    descZh: "DeepSeek API 终端界面客户端。",
  },
  {
    name: "claude-desktop-deepseek",
    url: "https://github.com/hustlxc/claude-desktop-deepseek",
    desc: "Claude Desktop with DeepSeek backend.",
    descZh: "使用 DeepSeek 后端的 Claude Desktop。",
  },
  {
    name: "deepclaude",
    url: "https://github.com/aattaran/deepclaude",
    desc: "DeepSeek + Claude dual-model proxy.",
    descZh: "DeepSeek + Claude 双模型代理。",
  },
  {
    name: "Ghostty",
    url: "https://github.com/ghostty-org/ghostty",
    desc: "Fast, feature-rich terminal emulator.",
    descZh: "快速、功能丰富的终端模拟器。",
  },
  {
    name: "cmux",
    url: "https://github.com/manaflow-ai/cmux",
    desc: "Session manager for Claude Code chats.",
    descZh: "Claude Code 会话管理器。",
  },
  {
    name: "yazi",
    url: "https://github.com/sxyazi/yazi",
    desc: "Blazing fast terminal file manager.",
    descZh: "极速终端文件管理器。",
  },
];

function renderTools(sectionEl, clr) {
  var grid = document.createElement("div");
  grid.className = "tool-grid";
  TOOLS.forEach(function(tool) {
    var card = document.createElement("a");
    card.className = "tool-card";
    card.href = tool.url;
    card.target = "_blank";
    card.rel = "noopener";

    // GitHub icon
    var iconWrapper = document.createElement("span");
    iconWrapper.className = "tool-gh-icon";
    var ghImg = document.createElement("img");
    ghImg.src = "https://unpkg.com/@lobehub/icons-static-svg@latest/icons/github.svg";
    ghImg.alt = "";
    ghImg.width = 18;
    ghImg.height = 18;
    iconWrapper.appendChild(ghImg);

    var name = document.createElement("strong");
    name.textContent = tool.name;

    var desc = document.createElement("span");
    desc.className = "tool-desc";
    desc.textContent = currentLang === "zh" ? tool.descZh : tool.desc;

    card.appendChild(iconWrapper);
    card.appendChild(name);
    card.appendChild(desc);
    grid.appendChild(card);
  });
  sectionEl.appendChild(grid);
}

function fieldKeyToProvider(key) {
  var map = {
    DEEPSEEK_API_KEY: "deepseek",
    NINEROUTER_API_KEY: "ninerouter",
    NINEROUTER_BASE_URL: "ninerouter",
    OMLX_API_KEY: "omlx",
    OMLX_BASE_URL: "omlx",
    NVIDIA_NIM_API_KEY: "nvidia_nim",
    NVIDIA_NIM_PROXY: "nvidia_nim",
    OPENROUTER_API_KEY: "open_router",
    OPENROUTER_PROXY: "open_router",
    KIMI_API_KEY: "kimi",
    KIMI_PROXY: "kimi",
    WAFER_API_KEY: "wafer",
    WAFER_PROXY: "wafer",
    OPENCODE_API_KEY: "opencode",
    OPENCODE_PROXY: "opencode",
    LM_STUDIO_BASE_URL: "lmstudio",
    LMSTUDIO_PROXY: "lmstudio",
    LLAMACPP_BASE_URL: "llamacpp",
    LLAMACPP_PROXY: "llamacpp",
    OLLAMA_BASE_URL: "ollama",
  };
  return map[key] || null;
}

function renderField(field, sectionId) {
  var wrapper = document.createElement("div");
  wrapper.className = "field" + (field.advanced ? " advanced-field" : "");
  wrapper.dataset.key = field.key;

  var label = document.createElement("label");
  label.htmlFor = "field-" + field.key;

  // Add provider icon for fields in the providers section
  var labelText = "<span>";
  if (sectionId === "providers") {
    var pid = fieldKeyToProvider(field.key);
    if (pid) {
      var iconUrl = providerIcon(pid);
      if (iconUrl) {
        labelText += '<img class="field-provider-icon" src="' + iconUrl + '" alt="" width="16" height="16" onerror="this.style.display=\'none\'" /> ';
      }
    }
  }
  labelText += field.label + "</span><span class=\"field-source\">" +
    sourceLabel(field.source) + (field.locked ? t("locked") : "") + "</span>";
  label.innerHTML = labelText;

  var input = inputForField(field);
  input.id = "field-" + field.key;
  input.dataset.key = field.key;
  input.dataset.original = field.value || "";
  input.dataset.secret = field.secret ? "true" : "false";
  input.dataset.configured = field.configured ? "true" : "false";
  input.disabled = field.locked;
  input.addEventListener("input", updateDirtyState);
  input.addEventListener("change", updateDirtyState);

  wrapper.append(label, input);
  if (field.description) {
    var desc = document.createElement("div");
    desc.className = "field-description";
    desc.textContent = field.description;
    wrapper.appendChild(desc);
  }
  return wrapper;
}

function inputForField(field) {
  if (field.type === "boolean") {
    var input = document.createElement("input");
    input.type = "checkbox";
    input.checked = String(field.value).toLowerCase() === "true";
    input.dataset.original = input.checked ? "true" : "false";
    return input;
  }

  if (field.type === "tri_boolean") {
    var select = document.createElement("select");
    [
      ["", t("inherit")],
      ["true", t("enabled")],
      ["false", t("disabled")],
    ].forEach(function(pair) { select.appendChild(option(pair[0], pair[1])); });
    select.value = field.value || "";
    return select;
  }

  if (field.type === "select") {
    var sel = document.createElement("select");
    field.options.forEach(function(v) { sel.appendChild(option(v, v)); });
    sel.value = field.value || (field.options[0] || "");
    return sel;
  }

  if (field.type === "textarea") {
    var ta = document.createElement("textarea");
    ta.value = field.value || "";
    return ta;
  }

  var inp = document.createElement("input");
  inp.type = field.type === "number" ? "number" : "text";
  if (field.type === "secret") {
    inp.type = "password";
    inp.placeholder = field.configured ? t("configuredPlaceholder") : t("notConfigured");
    inp.value = "";
    inp.autocomplete = "off";
  } else {
    inp.value = field.value || "";
  }
  if (field.key.indexOf("MODEL") === 0) {
    inp.setAttribute("list", "model-options");
  }
  return inp;
}

function option(value, label) {
  var o = document.createElement("option");
  o.value = value;
  o.textContent = label;
  return o;
}

/* ================================================================
   DIRTY STATE
   ================================================================ */
function readFieldValue(input) {
  if (input.type === "checkbox") return input.checked ? "true" : "false";
  if (input.dataset.secret === "true" && input.dataset.configured === "true") {
    return input.value ? input.value : MASKED_SECRET;
  }
  return input.value;
}

function changedValues() {
  var values = {};
  document.querySelectorAll("[data-key]").forEach(function(input) {
    if (input.disabled || !input.matches("input, select, textarea")) return;
    var value = readFieldValue(input);
    if (value !== input.dataset.original) {
      values[input.dataset.key] = value;
    }
  });
  return values;
}

function updateDirtyState() {
  var count = Object.keys(changedValues()).length;
  var msg = t("noChanges");
  if (count === 1) msg = count + t("unsaved1");
  else if (count > 1) msg = count + t("unsavedN");
  byId("dirtyState").textContent = msg;
  byId("applyButton").disabled = count === 0;
}

/* ================================================================
   VALIDATE / APPLY
   ================================================================ */
async function validate(showResult) {
  if (showResult === undefined) showResult = true;
  var result = await api("/admin/api/config/validate", {
    method: "POST",
    body: JSON.stringify({ values: changedValues() }),
  });
  byId("envPreview").textContent = result.env_preview || "";
  if (showResult) {
    showValidationResult(result);
  }
  return result;
}

function showValidationResult(result) {
  if (result.valid) {
    showMessage(t("msgValid"), "ok");
  } else {
    showMessage(result.errors.join("; "), "error");
  }
}

async function apply() {
  var result = await api("/admin/api/config/apply", {
    method: "POST",
    body: JSON.stringify({ values: changedValues() }),
  });
  byId("envPreview").textContent = result.env_preview || "";
  if (!result.applied) {
    showValidationResult(result);
    return;
  }
  var restart = result.restart || {};
  if (restart.required && restart.automatic) {
    showMessage(t("msgRestarting"), "ok");
    byId("applyButton").disabled = true;
    setTimeout(function() {
      window.location.href = restart.admin_url || "/admin";
    }, 1600);
    return;
  }
  var pending = restart.required ? restart.fields || [] : result.pending_fields || [];
  await load();
  showMessage(
    pending.length ? t("msgAppliedRestart") + pending.join(", ") : t("msgApplied"),
    "ok"
  );
}

/* ================================================================
   LOCAL STATUS
   ================================================================ */
async function refreshLocalStatus() {
  var result = await api("/admin/api/providers/local-status");
  result.providers.forEach(function(provider) {
    state.localStatus.set(provider.provider_id, provider);
    var meta = provider.status_code
      ? provider.base_url + " returned HTTP " + provider.status_code
      : provider.base_url;
    updateProviderCard(provider.provider_id, provider.status, statusLabel(provider.status), meta);
  });
}

async function testProvider(providerId, button) {
  var original = button.textContent;
  button.disabled = true;
  button.textContent = t("testing");
  try {
    var result = await api("/admin/api/providers/" + providerId + "/test", {
      method: "POST",
      body: "{}",
    });
    if (result.ok) {
      var modelCount = result.models.length;
      updateProviderCard(
        providerId,
        "reachable",
        modelCount + t("modelsCount"),
        result.models.slice(0, 3).join(", ") || t("noModels"),
      );
      state.modelOptions = Array.from(
        new Set(state.modelOptions.concat(result.models.map(function(m) { return providerId + "/" + m; }))),
      ).sort();
      syncModelDatalist();
    } else {
      updateProviderCard(providerId, "offline", result.error_type, result.error_type);
    }
  } finally {
    button.disabled = false;
    button.textContent = original;
  }
}

function syncModelDatalist() {
  var datalist = byId("model-options");
  if (!datalist) {
    datalist = document.createElement("datalist");
    datalist.id = "model-options";
    document.body.appendChild(datalist);
  }
  datalist.innerHTML = "";
  state.modelOptions.forEach(function(model) { datalist.appendChild(option(model, model)); });
}

/* ================================================================
   MESSAGES
   ================================================================ */
function showMessage(message, kind) {
  kind = kind || "";
  var area = byId("messageArea");
  area.textContent = message;
  area.className = "message-area " + kind;
}

/* ================================================================
   RESTORE DEEPSEEK V4 DEFAULTS
   ================================================================ */
function restoreDeepSeekDefaults() {
  var defaults = {
    MODEL: "deepseek/deepseek-v4-flash",
    MODEL_OPUS: "deepseek/deepseek-v4-pro",
    MODEL_SONNET: "deepseek/deepseek-v4-pro",
    MODEL_HAIKU: "deepseek/deepseek-v4-flash",
  };
  // Sonnet disables thinking for speed; others enable
  var thinkingOverrides = {
    ENABLE_MODEL_THINKING: "true",
    ENABLE_OPUS_THINKING: "",
    ENABLE_SONNET_THINKING: "false",
    ENABLE_HAIKU_THINKING: "",
  };
  Object.keys(thinkingOverrides).forEach(function(key) {
    var el = document.getElementById("field-" + key);
    if (el) {
      if (el.type === "checkbox") {
        el.checked = thinkingOverrides[key] === "true";
      } else {
        el.value = thinkingOverrides[key];
      }
      el.dispatchEvent(new Event("input", { bubbles: true }));
    }
  });
  Object.keys(defaults).forEach(function(key) {
    var el = document.getElementById("field-" + key);
    if (el) {
      el.value = defaults[key];
      el.dispatchEvent(new Event("input", { bubbles: true }));
    }
  });
  updateDirtyState();
  showMessage(t("dsRestored"), "ok");
}

/* ================================================================
   CLI COMMAND BUTTONS
   ================================================================ */
function isDeepSeekConfigured() {
  if (!state.config) return false;
  var fields = state.config.fields || [];
  for (var i = 0; i < fields.length; i++) {
    if (fields[i].key === "DEEPSEEK_API_KEY" && fields[i].configured) {
      return true;
    }
  }
  return false;
}

function handleCLICommand(cmd) {
  if (!isDeepSeekConfigured()) {
    if (!confirm(t("cliNoApiKey"))) return;
  }
  navigator.clipboard.writeText(cmd).then(function() {
    showMessage(cmd + " — " + t("cliCopied"), "ok");
  }).catch(function() {
    showMessage(cmd + " — " + t("cliCopied"), "ok");
  });
}

document.querySelectorAll(".cli-cmd").forEach(function(btn) {
  btn.addEventListener("click", function() {
    var cmd = btn.getAttribute("data-cmd");
    if (cmd) handleCLICommand(cmd);
  });
});

/* ================================================================
   INIT
   ================================================================ */
byId("validateButton").addEventListener("click", function() { validate(true); });
byId("applyButton").addEventListener("click", apply);
byId("refreshLocal").addEventListener("click", refreshLocalStatus);
byId("langToggle").addEventListener("click", toggleLang);

/* ---- Theme toggle ---- */
var currentTheme = (function(){
  try { return localStorage.getItem("fcc-theme") || "dark"; } catch(_) { return "dark"; }
})();
function applyTheme() {
  document.documentElement.setAttribute("data-theme", currentTheme);
  byId("themeToggle").textContent = currentTheme === "light" ? "☾" : "☀";
}
applyTheme();
byId("themeToggle").addEventListener("click", function() {
  currentTheme = currentTheme === "light" ? "dark" : "light";
  try { localStorage.setItem("fcc-theme", currentTheme); } catch(_) {}
  applyTheme();
});

/* ---- Env modal ---- */
byId("showEnvBtn").addEventListener("click", function() {
  byId("envModal").removeAttribute("hidden");
});
byId("closeEnvModal").addEventListener("click", function() {
  byId("envModal").setAttribute("hidden", "");
});
byId("envModal").addEventListener("click", function(e) {
  if (e.target === byId("envModal")) byId("envModal").setAttribute("hidden", "");
});

applyStaticTranslations();

load().catch(function(error) {
  byId("serverStatus").textContent = t("error");
  byId("serverStatus").className = "status-pill error";
  showMessage(error.message, "error");
});
