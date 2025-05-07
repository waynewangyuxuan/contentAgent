// Helper function to get the backend URL
const getBackendUrl = () => {
  return process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';
};

export async function fetchStatus() {
  const response = await fetch("/api/status")
  if (!response.ok) {
    throw new Error("Failed to fetch status")
  }
  return response.json()
}

// Direct API methods for use outside of API routes
export async function fetchStatusDirect() {
  const response = await fetch(`${getBackendUrl()}/status`)
  if (!response.ok) {
    throw new Error("Failed to fetch status")
  }
  return response.json()
}

export async function submitTaskDirect(task: string, context: any) {
  const response = await fetch(`${getBackendUrl()}/task`, {
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
  
  return response.json()
}
