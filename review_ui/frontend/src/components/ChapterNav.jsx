export default function ChapterNav({ chapters, selectedChapter, onSelect, showApproved, onToggleApproved }) {
  // Group chapters by module
  const modules = {}
  for (const ch of chapters) {
    if (!modules[ch.module_id]) {
      modules[ch.module_id] = { title: ch.module_title, chapters: [] }
    }
    modules[ch.module_id].chapters.push(ch)
  }

  return (
    <aside className="w-72 bg-white border-r border-gray-200 flex flex-col h-full overflow-hidden">
      <div className="px-4 py-3 border-b border-gray-200 shrink-0">
        <label className="flex items-center gap-2 text-sm text-gray-600 cursor-pointer select-none">
          <input
            type="checkbox"
            checked={showApproved}
            onChange={onToggleApproved}
            className="rounded"
          />
          Show approved
        </label>
      </div>

      <nav className="flex-1 overflow-y-auto py-2">
        {Object.entries(modules).map(([moduleId, mod]) => (
          <div key={moduleId} className="mb-2">
            <div className="px-4 py-1.5 text-xs font-semibold text-gray-400 uppercase tracking-wide">
              {mod.title}
            </div>
            {mod.chapters.map(ch => {
              const badge = showApproved ? ch.counts.approved : ch.counts.draft
              const isSelected = ch.chapter_id === selectedChapter
              return (
                <button
                  key={ch.chapter_id}
                  onClick={() => onSelect(ch.chapter_id)}
                  className={`w-full text-left px-4 py-2 flex items-start justify-between gap-2 text-sm transition-colors
                    ${isSelected
                      ? 'bg-indigo-50 text-indigo-700 font-medium'
                      : 'text-gray-700 hover:bg-gray-50'
                    }`}
                >
                  <span className="leading-snug">{ch.chapter_title}</span>
                  {badge > 0 && (
                    <span className={`shrink-0 mt-0.5 text-xs px-1.5 py-0.5 rounded-full font-medium
                      ${showApproved ? 'bg-green-100 text-green-700' : 'bg-amber-100 text-amber-700'}`}>
                      {badge}
                    </span>
                  )}
                </button>
              )
            })}
          </div>
        ))}
      </nav>
    </aside>
  )
}
