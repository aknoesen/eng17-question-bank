import { useEffect, useRef } from 'react'
import katex from 'katex'

// Splits a string into alternating text / math segments.
// Handles \(...\) inline and \[...\] display math.
function splitMath(text) {
  const parts = []
  const regex = /(\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\))/g
  let lastIndex = 0
  let match

  while ((match = regex.exec(text)) !== null) {
    if (match.index > lastIndex) {
      parts.push({ type: 'text', content: text.slice(lastIndex, match.index) })
    }
    const raw = match[0]
    const isDisplay = raw.startsWith('\\[')
    const inner = raw.slice(2, -2)
    parts.push({ type: 'math', content: inner, display: isDisplay, raw })
    lastIndex = match.index + raw.length
  }

  if (lastIndex < text.length) {
    parts.push({ type: 'text', content: text.slice(lastIndex) })
  }

  return parts
}

export default function KatexRenderer({ text }) {
  const containerRef = useRef(null)

  useEffect(() => {
    if (!containerRef.current || !text) return

    const container = containerRef.current
    container.innerHTML = ''

    const parts = splitMath(text)

    for (const part of parts) {
      const span = document.createElement('span')

      if (part.type === 'text') {
        span.textContent = part.content
      } else {
        try {
          span.innerHTML = katex.renderToString(part.content, {
            throwOnError: true,
            displayMode: part.display,
          })
        } catch {
          span.className = 'katex-error'
          span.textContent = part.raw
        }
      }

      container.appendChild(span)
    }
  }, [text])

  if (!text) return null

  return <span ref={containerRef} />
}
