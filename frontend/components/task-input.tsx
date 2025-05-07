"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Send, Sparkles } from "lucide-react"

interface TaskInputProps {
  onSubmit: (task: string) => void
  isLoading: boolean
}

export function TaskInput({ onSubmit, isLoading }: TaskInputProps) {
  const [task, setTask] = useState("")

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (task.trim() && !isLoading) {
      onSubmit(task.trim())
    }
  }

  const exampleTasks = [
    "Search for the latest news about Studio Ghibli",
    "Generate a tweet about sustainable living in a Ghibli style",
    "Find information about Hayao Miyazaki's latest film",
  ]

  const handleExampleClick = (example: string) => {
    setTask(example)
  }

  return (
    <div className="bg-white/80 backdrop-blur-sm rounded-xl p-6 shadow-md border border-emerald-100">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="task" className="block text-sm font-medium text-emerald-700 mb-2">
            What would you like me to help you with?
          </label>
          <Textarea
            id="task"
            placeholder="Describe your task here..."
            value={task}
            onChange={(e) => setTask(e.target.value)}
            className="min-h-[120px] border-emerald-200 focus:border-emerald-400 focus:ring-emerald-400"
          />
        </div>

        <div className="flex justify-between items-center">
          <div className="text-xs text-emerald-600">
            <span className="flex items-center gap-1">
              <Sparkles className="h-3 w-3" />
              Examples:
            </span>
            <div className="flex flex-wrap gap-2 mt-2">
              {exampleTasks.map((example, index) => (
                <button
                  key={index}
                  type="button"
                  onClick={() => handleExampleClick(example)}
                  className="text-xs px-2 py-1 bg-emerald-50 hover:bg-emerald-100 text-emerald-700 rounded-full transition-colors"
                >
                  {example.length > 30 ? example.substring(0, 30) + "..." : example}
                </button>
              ))}
            </div>
          </div>

          <Button
            type="submit"
            disabled={!task.trim() || isLoading}
            className="bg-emerald-600 hover:bg-emerald-700 text-white"
          >
            {isLoading ? (
              <>
                <div className="h-4 w-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                Processing...
              </>
            ) : (
              <>
                <Send className="h-4 w-4 mr-2" />
                Send Task
              </>
            )}
          </Button>
        </div>
      </form>
    </div>
  )
}
