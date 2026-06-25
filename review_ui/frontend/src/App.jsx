import { useState, useEffect } from 'react'
import ChapterNav from './components/ChapterNav.jsx'
import QuestionCard from './components/QuestionCard.jsx'

const API = 'http://localhost:8000'

export default function App() {
  const [chapters, setChapters] = useState([])
  const [selectedChapter, setSelectedChapter] = useState(null)
  const [questions, setQuestions] = useState([])
  const [showApproved, setShowApproved] = useState(false)
  const [summary, setSummary] = useState(null)
  const [loading, setLoading] = useState(false)

  // Load chapters and summary on mount
  useEffect(() => {
    loadChapters(true)
    loadSummary()
  }, [])

  // Reload questions when chapter or view mode changes
  useEffect(() => {
    if (selectedChapter === null) return
    loadQuestions(selectedChapter, showApproved ? 'approved' : 'draft')
  }, [selectedChapter, showApproved])

  async function loadChapters(selectDefault = false) {
    const res = await fetch(`${API}/api/chapters`)
    const data = await res.json()
    setChapters(data)
    if (selectDefault) {
      const first = data.find(c => c.counts.draft > 0) ?? data[0]
      if (first) setSelectedChapter(first.chapter_id)
    }
  }

  async function loadSummary() {
    const res = await fetch(`${API}/api/summary`)
    const data = await res.json()
    setSummary(data)
  }

  async function loadQuestions(chapterId, status) {
    setLoading(true)
    const url = `${API}/api/questions?chapter_id=${chapterId}&status=${status}`
    const res = await fetch(url)
    const data = await res.json()
    setQuestions(data)
    setLoading(false)
  }

  function handleChapterSelect(id) {
    setSelectedChapter(id)
    setShowApproved(false)
  }

  function handleReviewed(questionId) {
    setQuestions(prev => prev.filter(q => q.id !== questionId))
    // Refresh counts without resetting selected chapter
    loadChapters(false)
    loadSummary()
  }

  return (
    <div className="flex h-screen bg-gray-50 overflow-hidden">
      <ChapterNav
        chapters={chapters}
        selectedChapter={selectedChapter}
        onSelect={handleChapterSelect}
        showApproved={showApproved}
        onToggleApproved={() => setShowApproved(v => !v)}
      />

      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <header className="bg-white border-b border-gray-200 px-6 py-3 flex items-center justify-between shrink-0">
          <h1 className="text-lg font-bold text-gray-900 tracking-tight">VeriQAI Review</h1>
          {summary && (
            <div className="flex items-center gap-5 text-sm">
              <span className="text-green-600 font-medium">
                ✓ {summary.totals.approved} approved
              </span>
              <span className="text-gray-500">
                {summary.totals.draft} draft
              </span>
              {summary.totals.failed > 0 && (
                <span className="text-red-500">
                  ✕ {summary.totals.failed} rejected
                </span>
              )}
            </div>
          )}
        </header>

        {/* Content */}
        <main className="flex-1 overflow-y-auto p-6">
          {loading ? (
            <div className="text-center text-gray-400 mt-20 text-sm">Loading…</div>
          ) : questions.length === 0 ? (
            <div className="text-center mt-24">
              <div className="text-4xl mb-3 text-green-400">✓</div>
              <p className="text-gray-500">
                {showApproved
                  ? 'No approved questions for this chapter.'
                  : 'All questions reviewed for this chapter.'}
              </p>
            </div>
          ) : (
            <div className="space-y-5 max-w-3xl mx-auto">
              {questions.map(q => (
                <QuestionCard
                  key={q.id}
                  question={q}
                  onReviewed={handleReviewed}
                  readOnly={showApproved}
                />
              ))}
            </div>
          )}
        </main>
      </div>
    </div>
  )
}
