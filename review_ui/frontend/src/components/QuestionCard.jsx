import { useState } from 'react'
import KatexRenderer from './KatexRenderer.jsx'
import StatusBadge from './StatusBadge.jsx'

const API = 'http://localhost:8000'

const BLOOM_COLORS = {
  Remember:   'bg-blue-100 text-blue-700',
  Understand: 'bg-indigo-100 text-indigo-700',
  Apply:      'bg-violet-100 text-violet-700',
  Analyze:    'bg-amber-100 text-amber-700',
  Evaluate:   'bg-orange-100 text-orange-700',
  Create:     'bg-red-100 text-red-700',
}

const CHOICE_LABELS = ['A', 'B', 'C', 'D']

function DifficultyDots({ level }) {
  return (
    <span className="flex items-center gap-0.5">
      {[1, 2, 3, 4].map(i => (
        <span
          key={i}
          className={`w-2 h-2 rounded-full ${i <= level ? 'bg-gray-600' : 'bg-gray-200'}`}
        />
      ))}
    </span>
  )
}

function Collapsible({ label, children }) {
  const [open, setOpen] = useState(false)
  return (
    <div className="border border-gray-200 rounded">
      <button
        onClick={() => setOpen(v => !v)}
        className="w-full text-left px-3 py-2 text-sm font-medium text-gray-600 flex items-center justify-between hover:bg-gray-50"
      >
        {label}
        <span className="text-gray-400">{open ? '▲' : '▼'}</span>
      </button>
      {open && (
        <div className="px-3 py-2 text-sm text-gray-700 border-t border-gray-200">
          <KatexRenderer text={children} />
        </div>
      )}
    </div>
  )
}

export default function QuestionCard({ question: q, onReviewed, readOnly }) {
  const [removing, setRemoving] = useState(false)

  async function handleAction(status) {
    await fetch(`${API}/api/questions/${q.id}/status`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status }),
    })
    setRemoving(true)
    setTimeout(() => onReviewed(q.id), 400)
  }

  const bloomClass = BLOOM_COLORS[q.bloom_level] ?? 'bg-gray-100 text-gray-600'

  return (
    <div
      className={`bg-white border border-gray-200 rounded-lg p-5 shadow-sm space-y-3 transition-all duration-400
        ${removing ? 'opacity-0 scale-95' : 'opacity-100 scale-100'}`}
    >
      {/* Header row */}
      <div className="flex items-center gap-2 flex-wrap">
        <span className={`px-2 py-0.5 rounded text-xs font-medium ${bloomClass}`}>
          {q.bloom_level}
        </span>
        <DifficultyDots level={q.difficulty} />
        <StatusBadge status={q.status} />
        <span className="ml-auto text-xs text-gray-400">Q{q.question_number}</span>
      </div>

      {/* Topic line */}
      <div className="text-xs text-gray-400">
        {q.topic_title}{q.subtopic ? ` › ${q.subtopic}` : ''}
      </div>

      {/* Learning objective */}
      {q.learning_objective && (
        <div className="text-xs text-gray-400 italic">{q.learning_objective}</div>
      )}

      {/* Question text */}
      <div className="text-sm text-gray-800 leading-relaxed">
        <KatexRenderer text={q.question_text} />
      </div>

      {/* Choices */}
      <div className="space-y-1">
        {q.choices.map((choice, i) => (
          <div
            key={i}
            className={`flex items-start gap-2 px-3 py-2 rounded text-sm
              ${i === q.correct_answer_index ? 'bg-green-50 text-green-800' : 'text-gray-700'}`}
          >
            <span className={`font-semibold shrink-0 ${i === q.correct_answer_index ? 'text-green-700' : 'text-gray-400'}`}>
              {CHOICE_LABELS[i]}.
            </span>
            <KatexRenderer text={choice} />
          </div>
        ))}
      </div>

      {/* Collapsible feedback */}
      <Collapsible label="Correct feedback">{q.feedback_correct}</Collapsible>
      <Collapsible label="Incorrect feedback">{q.feedback_incorrect}</Collapsible>

      {/* Action buttons */}
      {!readOnly && (
        <div className="flex gap-3 pt-1">
          <button
            onClick={() => handleAction('approved')}
            disabled={removing}
            className="flex-1 py-2 rounded-md bg-green-600 hover:bg-green-700 text-white text-sm font-medium transition-colors disabled:opacity-50"
          >
            Approve
          </button>
          <button
            onClick={() => handleAction('failed')}
            disabled={removing}
            className="flex-1 py-2 rounded-md bg-red-600 hover:bg-red-700 text-white text-sm font-medium transition-colors disabled:opacity-50"
          >
            Reject
          </button>
        </div>
      )}
    </div>
  )
}
