<template>
  <div class="repo-detail">
    <div class="content-wrapper">
      <aside class="toc">
        <nav>
          <div
            v-for="(section, si) in sections"
            :key="`sec-${si}`"
            class="toc-section"
          >
            <div class="toc-title">{{ section.title }}</div>
            <div
              v-for="(item, ii) in section.items || []"
              :key="`item-${si}-${ii}`"
              class="toc-item"
              @click="selectItem(si, ii)"
              :aria-current="selected.section === si && selected.item === ii ? 'true' : undefined"
            >
              {{ item }}
            </div>
          </div>
        </nav>
      </aside>

      <main class="doc">
        <div class="doc-inner" ref="docInnerRef" v-html="content || ''"></div>
        <div v-if="showTop" class="fade fade-top" aria-hidden="true"></div>
        <div v-if="showBottom" class="fade fade-bottom" aria-hidden="true"></div>
      </main>
    </div>

    <div class="ask-row">
      <div class="ask-box">
        <input
          v-model="query"
          class="ask-input"
          :placeholder="placeholder"
          @keydown.enter.prevent="handleSend"
        />
        <button class="send-btn" @click="handleSend">Send-&gt;</button>
      </div>

      <button class="new-repo" @click="$emit('navigateNewRepo')" aria-label="New repo">
        <span class="plus">+</span>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick, watch } from 'vue'

const props = withDefaults(defineProps<{
  sections?: { title: string; items?: string[] }[]
  content?: string
  repoId?: string | null
  placeholder?: string
}>(), {
  sections: () => [
    { title: 'Introduction', items: ['sec1', 'sec2'] },
    { title: 'How to use', items: ['sec1', 'sec2'] }
  ],
  content: `Title
  
Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.`,
  repoId: null,
  placeholder: 'Try to ask me...'
})

const { sections, content, placeholder } = props

const docInnerRef = ref<HTMLElement | null>(null)
const showTop = ref(false)
const showBottom = ref(false)

const updateFades = () => {
  const el = docInnerRef.value
  if (!el) return
  showTop.value = el.scrollTop > 0
  // allow tiny rounding tolerance
  showBottom.value = el.scrollHeight > el.clientHeight && (el.scrollTop + el.clientHeight) < (el.scrollHeight - 1)
}

onMounted(() => {
  nextTick(() => {
    updateFades()
    const el = docInnerRef.value
    if (!el) return
    el.addEventListener('scroll', updateFades, { passive: true })
    window.addEventListener('resize', updateFades)
  })
})

onUnmounted(() => {
  const el = docInnerRef.value
  if (el) el.removeEventListener('scroll', updateFades)
  window.removeEventListener('resize', updateFades)
})

watch(() => content, () => {
  nextTick(updateFades)
})

const query = ref('')
const selected = ref<{ section: number | null; item: number | null }>({ section: null, item: null })

const selectItem = (si: number, ii: number) => {
  selected.value = { section: si, item: ii }
}

const emit = defineEmits<{
  (e: 'send', payload: string): void
  (e: 'navigateNewRepo'): void
}>()

const handleSend = () => {
  if (!query.value) return
  emit('send', query.value)
  query.value = ''
}
</script>

<style scoped>
.repo-detail {
  padding: 20px;
  box-sizing: border-box;
  min-height: 100vh;
  background: var(--container-bg);
  color: var(--text-color);
}

.content-wrapper {
  display: flex;
  gap: 24px;
  align-items: flex-start;
}

.toc {
  min-width: 100px;
  padding: 40px 40px;
  height: 80vh;
  overflow: auto;
  flex: 0 0 200px;
}

.toc nav {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.toc-section {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.toc-title {
  font-weight: 600;
  padding-left: 8px;
}

.toc-item {
  padding: 6px 8px;
  cursor: pointer;
  color: var(--text-color);
}

.toc-item[aria-current='true'] {
  background: var(--card-bg);
  border-radius: 6px;
  box-shadow: 0 1px 4px var(--shadow-color);
}

.doc {
  flex: 1 1 auto;
  border-left: 1px solid var(--border-color);
  min-height: 80vh;
  position: relative;
}

.doc-inner {
  /* leave space for header/other chrome and the fixed ask-row */
  max-height: calc(100vh - 160px);
  overflow: auto;
  padding: 40px 120px 40px 60px;
  background: transparent;
  line-height: 1.7;
  /* preserve newlines inside v-html content and allow long words to wrap */
  white-space: pre-wrap;
  overflow-wrap: break-word;
  word-break: break-word;
}

.fade {
  position: absolute;
  left: 0;
  right: 0;
  height: 48px;
  pointer-events: none;
  z-index: 8;
}

.fade-top {
  top: 0;
  background: linear-gradient(to bottom, var(--container-bg), transparent);
}

.fade-bottom {
  bottom: 0;
  background: linear-gradient(to top, var(--container-bg), transparent);
}

.ask-row {
  position: fixed;
  left: 20%;
  bottom: 5%;
  width: 60%;
  max-width: 960px;
  display: flex;
  align-items: center;
  gap: 16px;
  z-index: 1200;
}

.ask-box {
  flex: 1 1 auto;
  display: flex;
  height: 80px;
  align-items: center;
  background: var(--card-bg);
  border: 2px solid var(--border-color);
  border-radius: 20px;
  padding: 12px 18px;
  box-shadow: 0 2px 8px var(--shadow-color);
}

.ask-input {
  flex: 1 1 auto;
  border: none;
  outline: none;
  background: transparent;
  font-size: 16px;
  color: var(--text-color);
}

.send-btn {
  background: transparent;
  border: none;
  color: var(--text-color);
  cursor: pointer;
  font-weight: 600;
}

.new-repo {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: var(--card-bg);
  border: 2px solid var(--border-color);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 2px 8px var(--shadow-color);
}

.new-repo .plus {
  font-size: 24px;
  line-height: 1;
}
</style>