import { useEffect, useState } from "react"
import { useNavigate } from "react-router-dom"

const API_BASE_URL = "http://127.0.0.1:8000"

interface User {
  id: number
  name: string
  email: string
}

function Dashboard() {
  const navigate = useNavigate()

  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchUser() {
      const token = localStorage.getItem("access_token")

      if (!token) {
        navigate("/login")
        return
      }

      try {
        const response = await fetch(`${API_BASE_URL}/auth/me`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })

        if (!response.ok) {
          localStorage.removeItem("access_token")
          navigate("/login")
          return
        }

        const data = await response.json()
        setUser(data)
      } catch {
        localStorage.removeItem("access_token")
        navigate("/login")
      } finally {
        setLoading(false)
      }
    }

    fetchUser()
  }, [navigate])

  function handleLogout() {
    localStorage.removeItem("access_token")
    navigate("/login")
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-gray-500">Loading...</p>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-100">

      <nav className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">

          <h1 className="text-xl font-bold text-gray-900">
            AI Career Copilot
          </h1>

          <button
            onClick={handleLogout}
            className="px-4 py-2 text-sm font-medium text-gray-700 border rounded-lg hover:bg-gray-100"
          >
            Logout
          </button>

        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-6 py-10">

        <div className="bg-white rounded-2xl shadow-sm p-8 mb-8">
          <h2 className="text-3xl font-bold text-gray-900">
            Welcome, {user?.name}! 👋
          </h2>

          <p className="text-gray-500 mt-2">
            Your AI-powered career journey starts here.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">

          <div className="bg-white rounded-xl p-6 shadow-sm">
            <h3 className="font-semibold text-gray-900">
              Resume
            </h3>
            <p className="text-gray-500 text-sm mt-2">
              Upload and analyze your resume.
            </p>
          </div>

          <div className="bg-white rounded-xl p-6 shadow-sm">
            <h3 className="font-semibold text-gray-900">
              Job Matching
            </h3>
            <p className="text-gray-500 text-sm mt-2">
              Compare your resume with job descriptions.
            </p>
          </div>

          <div className="bg-white rounded-xl p-6 shadow-sm">
            <h3 className="font-semibold text-gray-900">
              AI Assistant
            </h3>
            <p className="text-gray-500 text-sm mt-2">
              Get AI-powered career guidance.
            </p>
          </div>

        </div>

      </main>
    </div>
  )
}

export default Dashboard