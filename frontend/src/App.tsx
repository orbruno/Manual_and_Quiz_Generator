import React, { useState } from 'react'
import UploadForm from './components/UploadForm'
import ManualDisplay from './components/ManualDisplay'
import Quiz, { QuizQuestion } from './components/Quiz'

interface ManualResponse {
  manual: string
}

const App: React.FC = () => {
  const [manual, setManual] = useState<string>('')
  const [quiz, setQuiz] = useState<QuizQuestion[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleGenerate = async (files: File[], prompt: string) => {
    setLoading(true)
    setError(null)
    setManual('')
    setQuiz([])

    try {
      // 1) Generate manual
      const formData = new FormData()
      files.forEach((f) => formData.append('files', f))
      formData.append('prompt', prompt)

      const mRes = await fetch('/api/manual', {
        method: 'POST',
        body: formData,
      })
      const mData: ManualResponse = await mRes.json()
      if (!mRes.ok) {
        throw new Error((mData as any).detail || mRes.statusText)
      }
      setManual(mData.manual)

      // 2) Generate quiz from the manual
      const qRes = await fetch('/api/quiz', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ manual: mData.manual }),
      })
      if (!qRes.ok) {
        const err = await qRes.json().catch(() => ({}))
        throw new Error((err as any).detail || qRes.statusText)
      }
      const qData: QuizQuestion[] = await qRes.json()
      setQuiz(qData)

    } catch (e: any) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-5xl mx-auto p-6">
      <h1 className="text-4xl font-extrabold text-center mb-8">
        Training Manual & Quiz Generator
      </h1>

      {/* Fixed 6-column grid: left=2, right=4 */}
      <div className="grid grid-cols-6 gap-6">
        {/* ─── Left panel (2/6) */}
        <div className="col-span-2 flex flex-col min-w-0">
          <UploadForm onGenerate={handleGenerate} loading={loading} />

          {error && (
            <p className="mt-4 text-red-500 font-medium">{error}</p>
          )}

          {quiz.length > 0 && (
            <div className="mt-8">
              <h2 className="text-2xl font-semibold mb-4">Quiz Time</h2>
              <Quiz quiz={quiz} />
            </div>
          )}
        </div>

        {/* ─── Right panel (4/6) */}
        <div className="col-span-4 min-w-0">
          {loading ? (
            <div className="h-full flex flex-col items-center justify-center p-8">
              <div
                className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mb-4"
                aria-label="Loading"
              />
              <p className="text-gray-500">
                Waiting for the manual to be generated…
              </p>
            </div>
          ) : manual ? (
            <section>
              <h2 className="text-2xl font-semibold mb-4">
                Generated Manual
              </h2>
              <ManualDisplay manual={manual} />
            </section>
          ) : (
            <div className="h-full flex items-center justify-center p-8 border-2 border-dashed border-gray-300 rounded-lg bg-gray-50 text-center">
              <p className="text-gray-500">
                Please upload at least two PDF or TXT files and enter your
                prompt on the left to generate a manual.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default App
