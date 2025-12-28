import React, { useState, useEffect } from 'react'
import { Toaster } from 'react-hot-toast'
import Header from './components/Header'
import UserSelector from './components/UserSelector'
import ChatInterface from './components/ChatInterface'
import DocumentList from './components/DocumentList'
import PermissionMatrix from './components/PermissionMatrix'
import SystemArchitecture from './components/SystemArchitecture'
import { fetchUsers, fetchDocuments } from './api/api'

function App() {
  const [currentUser, setCurrentUser] = useState('alice')
  const [users, setUsers] = useState([])
  const [documents, setDocuments] = useState([])
  const [activeTab, setActiveTab] = useState('chat')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadInitialData()
  }, [])

  const loadInitialData = async () => {
    try {
      setLoading(true)
      const [usersData, docsData] = await Promise.all([
        fetchUsers(),
        fetchDocuments()
      ])
      setUsers(usersData.users || [])
      setDocuments(docsData.documents || [])
    } catch (error) {
      console.error('Failed to load initial data:', error)
    } finally {
      setLoading(false)
    }
  }

  const refreshDocuments = async () => {
    try {
      const docsData = await fetchDocuments()
      setDocuments(docsData.documents || [])
    } catch (error) {
      console.error('Failed to refresh documents:', error)
    }
  }

  const tabs = [
    { id: 'chat', label: 'AI Agent Chat' },
    { id: 'documents', label: 'Documents' },
    { id: 'permissions', label: 'Permissions' },
    { id: 'architecture', label: 'System Architecture' }
  ]

  const handleTabChange = async (tabId) => {
    setActiveTab(tabId)
    if (tabId === 'documents') {
      await refreshDocuments()
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Toaster position="top-right" />
      
      <Header />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <UserSelector 
          users={users}
          currentUser={currentUser}
          onUserChange={setCurrentUser}
        />

        <div className="mt-6 bg-white rounded-lg shadow">
          <div className="border-b border-gray-200">
            <nav className="flex -mb-px">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => handleTabChange(tab.id)}
                  className={`px-6 py-4 text-sm font-medium border-b-2 transition-colors ${
                    activeTab === tab.id
                      ? 'border-blue-600 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  {tab.label}
                </button>
              ))}
            </nav>
          </div>

          <div className="p-6">
            {loading ? (
              <div className="flex items-center justify-center py-12">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
              </div>
            ) : (
              <>
                {activeTab === 'chat' && (
                  <ChatInterface 
                    currentUser={currentUser}
                    onDocumentChange={refreshDocuments}
                  />
                )}
                {activeTab === 'documents' && (
                  <DocumentList documents={documents} onRefresh={refreshDocuments} />
                )}
                {activeTab === 'permissions' && (
                  <PermissionMatrix users={users} />
                )}
                {activeTab === 'architecture' && (
                  <SystemArchitecture />
                )}
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
