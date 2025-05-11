import React, { useState } from 'react'

export interface QuizQuestion {
  question: string
  answers: string[]
  correctAnswer: number[]
}

type Props = {
  quiz: QuizQuestion[]
}

const Quiz: React.FC<Props> = ({ quiz }) => {
  const [current, setCurrent] = useState(0)
  const [selected, setSelected] = useState<number[]>([])
  const [score, setScore] = useState(0)
  const [showResult, setShowResult] = useState(false)

  const q = quiz[current]
  const isMulti = q.correctAnswer.length > 1

  const toggleAnswer = (idx: number) => {
    if (isMulti) {
      // multi‐choice: toggle in/out
      setSelected((prev) =>
        prev.includes(idx) ? prev.filter((i) => i !== idx) : [...prev, idx]
      )
    } else {
      // single‐choice: replace
      setSelected([idx])
    }
  }

  const handleNext = () => {
    // check correctness (sort to compare)
    const sortedSel = [...selected].sort()
    const sortedCorrect = [...q.correctAnswer].sort()
    const correct =
      sortedSel.length === sortedCorrect.length &&
      sortedSel.every((v, i) => v === sortedCorrect[i])

    if (correct) setScore((s) => s + 1)

    if (current + 1 < quiz.length) {
      // move to next question
      setCurrent((c) => c + 1)
      setSelected([])
    } else {
      // finished all questions
      setShowResult(true)
    }
  }

  if (showResult) {
    return (
      <div className="p-4 border rounded bg-green-50">
        <h3 className="text-2xl font-bold mb-2">Your Score</h3>
        <p className="text-lg">
          {score} of {quiz.length} correct
        </p>
      </div>
    )
  }

  return (
    <div className="p-4 border rounded bg-white">
      <p className="font-semibold mb-4">
        Question {current + 1} of {quiz.length}
      </p>
      <p className="mb-4">{q.question}</p>

      <div className="space-y-2">
        {q.answers.map((ans, i) => (
          <label key={i} className="flex items-center space-x-2">
            <input
              type={isMulti ? 'checkbox' : 'radio'}
              name={`q${current}`}
              checked={selected.includes(i)}
              onChange={() => toggleAnswer(i)}
            />
            <span>{ans}</span>
          </label>
        ))}
      </div>

      <button
        onClick={handleNext}
        disabled={selected.length === 0}
        className="mt-6 px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50"
      >
        {current + 1 === quiz.length ? 'Submit' : 'Next'}
      </button>
    </div>
  )
}

export default Quiz