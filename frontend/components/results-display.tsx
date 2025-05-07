import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import type { TaskResult } from "@/components/agent-dashboard"
import { CheckCircle, XCircle, AlertCircle } from "lucide-react"
import { Badge } from "@/components/ui/badge"

interface ResultsDisplayProps {
  result: TaskResult
}

export function ResultsDisplay({ result }: ResultsDisplayProps) {
  const isSuccess = result.result?.success
  const toolName = result.plan?.tool_name

  return (
    <Card className="bg-white/80 backdrop-blur-sm border-emerald-100">
      <CardHeader className="pb-2">
        <CardTitle className="text-lg flex items-center justify-between text-emerald-800">
          <span>Task Result</span>
          {isSuccess !== undefined &&
            (isSuccess ? (
              <Badge className="bg-green-100 text-green-800 hover:bg-green-100 flex items-center gap-1">
                <CheckCircle className="h-3.5 w-3.5" />
                Success
              </Badge>
            ) : (
              <Badge className="bg-red-100 text-red-800 hover:bg-red-100 flex items-center gap-1">
                <XCircle className="h-3.5 w-3.5" />
                Failed
              </Badge>
            ))}
        </CardTitle>
      </CardHeader>
      <CardContent>
        {result.error ? (
          <div className="bg-red-50 p-4 rounded-lg flex items-start gap-3">
            <AlertCircle className="h-5 w-5 text-red-500 mt-0.5" />
            <div>
              <p className="font-medium text-red-700">Error Occurred</p>
              <p className="text-sm text-red-600 mt-1">{result.error}</p>
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            {toolName && (
              <div className="bg-emerald-50 p-3 rounded-lg">
                <p className="text-sm font-medium text-emerald-700">Tool Used</p>
                <p className="text-emerald-600">{toolName.replace(/_/g, " ")}</p>

                {result.plan?.parameters && (
                  <div className="mt-2">
                    <p className="text-xs font-medium text-emerald-700">Parameters:</p>
                    <pre className="text-xs bg-emerald-100/50 p-2 rounded mt-1 overflow-x-auto">
                      {JSON.stringify(result.plan.parameters, null, 2)}
                    </pre>
                  </div>
                )}
              </div>
            )}

            {result.result && (
              <div>
                <p className="text-sm font-medium text-emerald-700 mb-2">Result:</p>
                <ResultContent result={result.result} />
              </div>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  )
}

function ResultContent({ result }: { result: any }) {
  // Handle different result types
  if (typeof result === "string") {
    return <p className="text-emerald-700">{result}</p>
  }

  if (result.text) {
    return <p className="text-emerald-700">{result.text}</p>
  }

  if (result.html) {
    return (
      <div
        className="prose prose-sm max-w-none prose-headings:text-emerald-800 prose-a:text-emerald-600"
        dangerouslySetInnerHTML={{ __html: result.html }}
      />
    )
  }

  // For search results or other structured data
  if (result.items || result.results) {
    const items = result.items || result.results
    return (
      <ul className="space-y-3">
        {items.map((item: any, index: number) => (
          <li key={index} className="bg-white/50 p-3 rounded-lg border border-emerald-50">
            {item.title && <p className="font-medium text-emerald-800">{item.title}</p>}
            {item.description && <p className="text-sm text-emerald-600 mt-1">{item.description}</p>}
            {item.url && (
              <a
                href={item.url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-xs text-emerald-500 hover:text-emerald-700 mt-1 inline-block"
              >
                {item.url}
              </a>
            )}
          </li>
        ))}
      </ul>
    )
  }

  // Default: show as JSON
  return (
    <pre className="text-xs bg-emerald-50 p-3 rounded overflow-x-auto text-emerald-700">
      {JSON.stringify(result, null, 2)}
    </pre>
  )
}
