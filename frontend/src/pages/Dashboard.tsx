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
  const [resumeFile, setResumeFile] = useState<File | null>(null)
  const [uploading, setUploading] = useState(false)
  const [resumeText, setResumeText] = useState("")
  const [uploadError, setUploadError] = useState("")

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
  

  async function handleResumeUpload() {
    alert("Upload button clicked")

  if (!resumeFile) {
    setUploadError("Please select a PDF file.")
    return
  }

  setUploadError("")
  setUploading(true)

  const formData = new FormData()
  formData.append("file", resumeFile)

  try {
    const response = await fetch(`${API_BASE_URL}/resume/upload`, {
      method: "POST",
      body: formData,
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.detail || "Resume upload failed")
    }

    setResumeText(data.text)

    console.log("Resume uploaded successfully:", data)
  } catch (error) {
    setUploadError(
      error instanceof Error
        ? error.message
        : "Resume upload failed"
    )
  } finally {
    setUploading(false)
  }
}

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

        <div className="bg-white rounded-2xl shadow-sm p-8 mb-8">

            <h2 className="text-2xl font-bold text-gray-900">
              Upload Your Resume
            </h2>

            <p className="text-gray-500 mt-2 mb-6">
              Upload your resume PDF to extract and analyze its content.
            </p>

            <div className="flex flex-col md:flex-row gap-4 items-start md:items-center">

                <input
                    type="file"
                    accept=".pdf,application/pdf"
                    onChange={(e) => {
                        setResumeFile(e.target.files?.[0] || null)
                        setUploadError("")
                    }}
                    className="block w-full text-sm text-gray-600"
                />

                <button
                    onClick={handleResumeUpload}
                    disabled={uploading || !resumeFile}
                    className="px-6 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition disabled:opacity-50"
                >
                    {uploading ? "Uploading..." : "Upload Resume"}
                </button>

            </div>

            {resumeFile && (
                <p className="text-sm text-gray-500 mt-4">
                    Selected: {resumeFile.name}
                </p>
            )}

            {uploadError && (
                <div className="mt-4 p-3 rounded-lg bg-red-100 text-red-700 text-sm">
                    {uploadError}
                </div>
            )}

        </div>

        {resumeText && (
            <div className="bg-white rounded-2xl shadow-sm p-8 mb-8">
                <h2 className="text-2xl font-bold text-gray-900">
                    Extracted Resume Text
                </h2>

                <pre className="mt-4 p-4 bg-gray-50 rounded-lg text-sm text-gray-700 whitespace-pre-wrap overflow-x-auto">
                    {resumeText}
                </pre>
            </div>
        )}

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