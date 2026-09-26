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

  // Stage 2: Job Description
  const [jobDescription, setJobDescription] = useState("")
  const [jobAnalysis, setJobAnalysis] = useState<any>(null)
  const [matchAnalysis, setMatchAnalysis] = useState<any>(null);
  const [matchingJob, setMatchingJob] = useState(false);
  const [tailoredResume, setTailoredResume] = useState<any>(null);
  const [tailoringResume, setTailoringResume] = useState(false);
  const [analyzingJob, setAnalyzingJob] = useState(false)

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
    if (!resumeFile) {
      setUploadError("Please select a PDF file.")
      return
    }

    setUploadError("")
    setUploading(true)

    const formData = new FormData()
    formData.append("file", resumeFile)

    try {
      const token = localStorage.getItem("access_token")

      const response = await fetch(`${API_BASE_URL}/resume/upload`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
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

  async function handleJobAnalysis() {
    if (!jobDescription.trim()) {
      return
    }

    setAnalyzingJob(true)
    setJobAnalysis("")

    try {
      const response = await fetch(`${API_BASE_URL}/job/analyze`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          job_description: jobDescription,
        }),
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.detail || "Job analysis failed")
    }

    setJobAnalysis(data.analysis)
  } catch (error) {
    setJobAnalysis(
      error instanceof Error
        ? error.message
        : "Job analysis failed"
    )
  } finally {
    setAnalyzingJob(false)
  }
}

const handleResumeMatching = async () => {
  if (!jobDescription.trim()) {
    alert("Please enter a job description first.");
    return;
  }

  setMatchingJob(true);

  try {
    const token = localStorage.getItem("access_token");

    const response = await fetch("http://127.0.0.1:8000/job/match", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        job_description: jobDescription,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Failed to match resume");
    }

    setMatchAnalysis(data.analysis);
  } catch (error: any) {
    alert(error.message);
  } finally {
    setMatchingJob(false);
  }
};

const handleResumeTailoring = async () => {
  if (!jobDescription.trim()) {
    alert("Please enter a job description first.");
    return;
  }

  setTailoringResume(true);

  try {
    const token = localStorage.getItem("access_token");

    const response = await fetch(
      "http://127.0.0.1:8000/job/tailor",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          job_description: jobDescription,
        }),
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        data.detail || "Failed to tailor resume"
      );
    }

    setTailoredResume(data.analysis);
  } catch (error: any) {
    alert(error.message);
  } finally {
    setTailoringResume(false);
  }
};

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

        {/* Welcome Section */}

        <div className="bg-white rounded-2xl shadow-sm p-8 mb-8">
          <h2 className="text-3xl font-bold text-gray-900">
            Welcome, {user?.name}! 👋
          </h2>

          <p className="text-gray-500 mt-2">
            Your AI-powered career journey starts here.
          </p>
        </div>

        {/* Resume Upload Section */}

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

        {/* Extracted Resume Text */}

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

        {/* Stage 2: Job Description */}

        <div className="bg-white rounded-2xl shadow-sm p-8 mb-8">

          <h2 className="text-2xl font-bold text-gray-900">
            Job Description
          </h2>

          <p className="text-gray-500 mt-2">
            Paste the job description you want to analyze against your resume.
          </p>

          <textarea
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            placeholder="Paste the job description here..."
            className="mt-4 w-full h-64 p-4 border border-gray-300 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
          />

          <button
            onClick={handleJobAnalysis}
            disabled={!jobDescription.trim() || analyzingJob}
            className="mt-4 px-6 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition disabled:opacity-50"
          >
            {analyzingJob ? "Analyzing..." : "Analyze Job"}
          </button>

          <button
            onClick={handleResumeMatching}
            disabled={matchingJob}
            className="mt-4 ml-3 px-6 py-3 bg-green-600 text-white rounded-lg font-semibold hover:bg-green-700 transition disabled:opacity-50"
          >
            {matchingJob ? "Matching..." : "Match Resume"}
          </button>

          <button
            onClick={handleResumeTailoring}
            disabled={tailoringResume}
            className="mt-4 ml-3 px-6 py-3 bg-purple-600 text-white rounded-lg font-semibold hover:bg-purple-700 transition disabled:opacity-50"
          >
            {tailoringResume ? "Tailoring..." : "Tailor Resume"}
          </button>

          {jobAnalysis && (
            <div className="mt-6 p-6 bg-gray-50 rounded-lg">
              <h3 className="text-xl font-bold text-gray-900">
                Job Analysis
              </h3>

              {/* Job Title */}
              <div className="mt-5">
                <h4 className="font-semibold text-gray-900">
                  Job Title
                </h4>
                <p className="mt-1 text-gray-700">
                  {jobAnalysis.job_title}
                </p>
              </div>

              {/* Technical Skills */}
              <div className="mt-5">
                <h4 className="font-semibold text-gray-900">
                  Technical Skills
                </h4>

                <div className="flex flex-wrap gap-2 mt-2">
                  {jobAnalysis.technical_skills?.map(
                    (skill: string, index: number) => (
                      <span
                        key={index}
                        className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm"
                      >
                        {skill}
                      </span>
                    )
                  )}
                </div>
              </div>

              {/* Responsibilities */}
              <div className="mt-5">
                <h4 className="font-semibold text-gray-900">
                  Responsibilities
                </h4>

                <div className="mt-2 space-y-2">
                  {jobAnalysis.responsibilities &&
                  jobAnalysis.responsibilities.length > 0 ? (
                    jobAnalysis.responsibilities.map(
                      (responsibility: string, index: number) => (
                        <div
                          key={index}
                          className="p-3 bg-white border border-gray-200 rounded-lg text-gray-700"
                        >
                          • {responsibility}
                        </div>
                      )
                    )
                  ) : (
                    <p className="text-gray-500">
                      No responsibilities specified.
                    </p>
                  )}
                </div>
              </div>

              {/* Experience */}
              <div className="mt-5">
                <h4 className="font-semibold text-gray-900">
                  Required Experience
                </h4>
                <p className="mt-1 text-gray-700">
                  {jobAnalysis.experience}
                </p>
              </div>

              {/* Education */}
              <div className="mt-5">
                <h4 className="font-semibold text-gray-900">
                  Education Requirements
                </h4>
                <p className="mt-1 text-gray-700">
                  {jobAnalysis.education}
                </p>
              </div>

              {/* Keywords */}
              <div className="mt-5">
                <h4 className="font-semibold text-gray-900">
                  Important Keywords
                </h4>

                <div className="flex flex-wrap gap-2 mt-2">
                  {jobAnalysis.keywords?.map(
                    (keyword: string, index: number) => (
                      <span
                        key={index}
                        className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm"
                      >
                        {keyword}
                      </span>
                    )
                  )}
                </div>
              </div>
            </div>
          )}

          {matchAnalysis && (
            <div className="mt-6 p-6 bg-green-50 rounded-lg">
              <h3 className="text-xl font-bold text-gray-900">
                Resume Match Analysis
              </h3>

              {/* Match Percentage */}
              <div className="mt-5">
                <h4 className="font-semibold text-gray-900">
                  Match Percentage
                </h4>
                <p className="mt-1 text-3xl font-bold text-green-600">
                  {matchAnalysis.match_percentage}%
                </p>
              </div>

              {/* Matching Skills */}
              <div className="mt-5">
                <h4 className="font-semibold text-gray-900">
                  Matching Skills
                </h4>

                <div className="flex flex-wrap gap-2 mt-2">
                  {matchAnalysis.matching_skills?.map(
                    (skill: string, index: number) => (
                      <span
                        key={index}
                        className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm"
                      >
                        {skill}
                      </span>
                    )
                  )}
                </div>
              </div>

              {/* Missing Skills */}
              <div className="mt-5">
                <h4 className="font-semibold text-gray-900">
                  Missing Skills
                </h4>

                <div className="flex flex-wrap gap-2 mt-2">
                  {matchAnalysis.missing_skills?.map(
                    (skill: string, index: number) => (
                      <span
                        key={index}
                        className="px-3 py-1 bg-red-100 text-red-700 rounded-full text-sm"
                      >
                        {skill}
                      </span>
                    )
                  )}
                </div>
              </div>

              {/* Strengths */}
              <div className="mt-5">
                <h4 className="font-semibold text-gray-900">
                  Strengths
                </h4>

                <div className="mt-2 space-y-2">
                  {matchAnalysis.strengths?.map(
                    (strength: string, index: number) => (
                      <div
                        key={index}
                        className="p-3 bg-white border border-gray-200 rounded-lg text-gray-700"
                      >
                        • {strength}
                      </div>
                    )
                  )}
                </div>
              </div>

              {/* Skill Gaps */}
              <div className="mt-5">
                <h4 className="font-semibold text-gray-900">
                  Skill Gaps
                </h4>

                <div className="mt-2 space-y-2">
                  {matchAnalysis.skill_gaps?.map(
                    (gap: string, index: number) => (
                      <div
                        key={index}
                        className="p-3 bg-white border border-gray-200 rounded-lg text-gray-700"
                      >
                        • {gap}
                      </div>
                    )
                  )}
                </div>
              </div>

              {/* Suggestions */}
              <div className="mt-5">
                <h4 className="font-semibold text-gray-900">
                  Suggestions
                </h4>

                <div className="mt-2 space-y-2">
                  {matchAnalysis.suggestions?.map(
                    (suggestion: string, index: number) => (
                      <div
                        key={index}
                        className="p-3 bg-white border border-gray-200 rounded-lg text-gray-700"
                      >
                        • {suggestion}
                      </div>
                    )
                  )}
                </div>
              </div>
            </div>
          )}

        {tailoredResume && (
          <div className="mt-6 p-6 bg-purple-50 rounded-lg">
            <h3 className="text-xl font-bold text-gray-900">
              AI Tailored Resume
            </h3>

            {/* Professional Summary */}
            <div className="mt-5">
              <h4 className="font-semibold text-gray-900">
                Professional Summary
              </h4>

              <p className="mt-2 p-4 bg-white border border-gray-200 rounded-lg text-gray-700">
                {tailoredResume.professional_summary}
              </p>
            </div>

            {/* Technical Skills */}
            <div className="mt-5">
              <h4 className="font-semibold text-gray-900">
                Technical Skills
              </h4>

              <div className="flex flex-wrap gap-2 mt-2">
                {tailoredResume.technical_skills?.map(
                  (skill: string, index: number) => (
                    <span
                      key={index}
                      className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm"
                    >
                      {skill}
                    </span>
                  )
                )}
              </div>
            </div>

            {/* Project Highlights */}
            <div className="mt-5">
              <h4 className="font-semibold text-gray-900">
                Project Highlights
              </h4>

              <div className="mt-2 space-y-2">
                {tailoredResume.project_highlights?.map(
                  (project: string, index: number) => (
                    <div
                      key={index}
                      className="p-3 bg-white border border-gray-200 rounded-lg text-gray-700"
                    >
                      • {project}
                    </div>
                  )
                )}
              </div>
            </div>

            {/* Resume Improvements */}
            <div className="mt-5">
              <h4 className="font-semibold text-gray-900">
                Resume Improvements
              </h4>

              <div className="mt-2 space-y-2">
                {tailoredResume.resume_improvements?.map(
                  (improvement: string, index: number) => (
                    <div
                      key={index}
                      className="p-3 bg-white border border-gray-200 rounded-lg text-gray-700"
                    >
                      • {improvement}
                    </div>
                  )
                )}
              </div>
            </div>
          </div>
        )}  

        </div>

        {/* Dashboard Cards */}

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