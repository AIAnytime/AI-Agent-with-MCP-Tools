import React from 'react'
import { FileText, RefreshCw, Calendar, User } from 'lucide-react'
import toast from 'react-hot-toast'

function DocumentList({ documents, onRefresh }) {
  const handleRefresh = async () => {
    try {
      await onRefresh()
      toast.success('Documents refreshed')
    } catch (error) {
      toast.error('Failed to refresh documents')
    }
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleString()
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-semibold text-gray-900">Document Storage</h2>
        <button
          onClick={handleRefresh}
          className="px-4 py-2 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors flex items-center space-x-2"
        >
          <RefreshCw className="h-4 w-4" />
          <span>Refresh</span>
        </button>
      </div>

      {documents.length === 0 ? (
        <div className="text-center py-12 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300">
          <FileText className="h-12 w-12 text-gray-400 mx-auto mb-3" />
          <p className="text-gray-600 font-medium">No documents found</p>
          <p className="text-sm text-gray-500 mt-1">Create a document using the AI Agent Chat</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-4">
          {documents.map((doc) => (
            <div
              key={doc.id}
              className="bg-white border border-gray-200 rounded-lg p-5 hover:shadow-md transition-shadow"
            >
              <div className="flex items-start justify-between">
                <div className="flex items-start space-x-3 flex-1">
                  <div className="flex-shrink-0 h-10 w-10 bg-blue-100 rounded-lg flex items-center justify-center">
                    <FileText className="h-5 w-5 text-blue-600" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <h3 className="text-lg font-semibold text-gray-900 mb-1">{doc.id}</h3>
                    <p className="text-sm text-gray-600 mb-3">{doc.content_preview}</p>
                    <div className="flex items-center space-x-4 text-xs text-gray-500">
                      <div className="flex items-center space-x-1">
                        <User className="h-3 w-3" />
                        <span>{doc.created_by}</span>
                      </div>
                      <div className="flex items-center space-x-1">
                        <Calendar className="h-3 w-3" />
                        <span>Created: {formatDate(doc.created_at)}</span>
                      </div>
                    </div>
                    {doc.updated_at !== doc.created_at && (
                      <div className="text-xs text-gray-500 mt-1">
                        Updated: {formatDate(doc.updated_at)}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default DocumentList
