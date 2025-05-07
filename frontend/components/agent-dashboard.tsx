"use client"

import { useState, useEffect } from "react"
import { TaskInput } from "@/components/task-input"
import { StatusPanel } from "@/components/status-panel"
import { ResultsDisplay } from "@/components/results-display"
import { MemoryVisualizer } from "@/components/memory-visualizer"
import { AgentThinking } from "@/components/agent-thinking"
import { ToolsPanel } from "@/components/tools-panel"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Toaster } from "@/components/ui/toaster"
import { useToast } from "@/hooks/use-toast"
import { fetchStatus } from "@/lib/api"

export type AgentStatus = {
  status: string
  available_tools: {
    [key: string]: string
  }
  memory_stats: {
    content_count: number
    facts_count: number
  }
}

export type TaskResult = {
  plan?: {
    tool_name: string
    parameters: any
  }
  result?: {
    success: boolean
    [key: string]: any
  }
  updated_context?: any
  error?: string
}

export function AgentDashboard() {
  const [status, setStatus] = useState<AgentStatus | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [isThinking, setIsThinking] = useState(false)
  const [taskResult, setTaskResult] = useState<TaskResult | null>(null)
  const [context, setContext] = useState<any>({})
  const [history, setHistory] = useState<Array<{ task: string; result: TaskResult }>>([])
  const { toast } = useToast()

  useEffect(() => {
    const fetchAgentStatus = async () => {
      try {
        const data = await fetchStatus()
        setStatus(data)
      } catch (error) {
        toast({
          title: "Connection Error",
          description: "Could not connect to the agent. Please try again later.",
          variant: "destructive",
        })
      }
    }

    fetchAgentStatus()
    const interval = setInterval(fetchAgentStatus, 30000) // Poll every 30 seconds

    return () => clearInterval(interval)
  }, [toast])

  const handleTaskSubmit = async (task: string) => {
    setIsLoading(true)
    setIsThinking(true)

    try {
      const response = await fetch("/api/task", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          task,
          context,
        }),
      })

      if (!response.ok) {
        throw new Error("Failed to execute task")
      }

      const result: TaskResult = await response.json()

      // Simulate thinking time for better UX
      setTimeout(() => {
        setIsThinking(false)
        setTaskResult(result)

        if (result.updated_context) {
          setContext(result.updated_context)
        }

        setHistory((prev) => [...prev, { task, result }])

        toast({
          title: "Task Complete",
          description: result.error
            ? `Error: ${result.error}`
            : `Successfully executed using ${result.plan?.tool_name || "unknown tool"}`,
          variant: result.error ? "destructive" : "default",
        })

        setIsLoading(false)
      }, 2000)
    } catch (error) {
      setIsThinking(false)
      setIsLoading(false)
      toast({
        title: "Task Failed",
        description: error instanceof Error ? error.message : "An unknown error occurred",
        variant: "destructive",
      })
    }
  }

  return (
    <div className="space-y-8 pb-20">
      <header className="text-center mb-12">
        <h1 className="text-4xl md:text-5xl font-bold tracking-tight mb-2 text-emerald-800 drop-shadow-sm">
          Ghibli Agent
        </h1>
        <p className="text-lg text-emerald-700/80 max-w-2xl mx-auto">
          A magical assistant powered by AI, ready to help with your tasks
        </p>
      </header>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <TaskInput onSubmit={handleTaskSubmit} isLoading={isLoading} />

          {isThinking && <AgentThinking />}

          {!isThinking && taskResult && (
            <div className="mt-8 animate-fade-in">
              <ResultsDisplay result={taskResult} />
            </div>
          )}
        </div>

        <div className="space-y-6">
          <StatusPanel status={status} />
          <ToolsPanel tools={status?.available_tools || {}} />
        </div>
      </div>

      <Tabs defaultValue="memory" className="mt-12">
        <TabsList className="grid w-full max-w-md mx-auto grid-cols-2">
          <TabsTrigger value="memory">Memory & Context</TabsTrigger>
          <TabsTrigger value="history">Task History</TabsTrigger>
        </TabsList>
        <TabsContent value="memory" className="mt-6">
          <MemoryVisualizer memoryStats={status?.memory_stats} context={context} />
        </TabsContent>
        <TabsContent value="history" className="mt-6">
          <div className="bg-white/80 backdrop-blur-sm rounded-xl p-6 shadow-md border border-emerald-100">
            {history.length === 0 ? (
              <div className="text-center py-8 text-emerald-700/70">
                <p>No tasks have been performed yet.</p>
                <p className="text-sm mt-2">Your task history will appear here.</p>
              </div>
            ) : (
              <ul className="space-y-4 max-h-96 overflow-y-auto pr-2">
                {history.map((item, index) => (
                  <li key={index} className="border-b border-emerald-100 pb-4">
                    <p className="font-medium text-emerald-800">{item.task}</p>
                    <p className="text-sm text-emerald-600 mt-1">Tool: {item.result.plan?.tool_name || "Unknown"}</p>
                    {item.result.result?.success ? (
                      <span className="inline-block px-2 py-1 text-xs rounded bg-emerald-100 text-emerald-800 mt-2">
                        Success
                      </span>
                    ) : (
                      <span className="inline-block px-2 py-1 text-xs rounded bg-red-100 text-red-800 mt-2">
                        Failed
                      </span>
                    )}
                  </li>
                ))}
              </ul>
            )}
          </div>
        </TabsContent>
      </Tabs>

      <Toaster />
    </div>
  )
}
