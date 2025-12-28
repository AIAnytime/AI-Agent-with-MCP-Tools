import React from 'react'
import { User, ShieldCheck, Edit, Eye } from 'lucide-react'

function UserSelector({ users, currentUser, onUserChange }) {
  const getRoleIcon = (role) => {
    switch (role) {
      case 'admin':
        return <ShieldCheck className="h-4 w-4" />
      case 'editor':
        return <Edit className="h-4 w-4" />
      case 'viewer':
        return <Eye className="h-4 w-4" />
      default:
        return <User className="h-4 w-4" />
    }
  }

  const getRoleColor = (role) => {
    switch (role) {
      case 'admin':
        return 'bg-purple-100 text-purple-700 border-purple-200'
      case 'editor':
        return 'bg-blue-100 text-blue-700 border-blue-200'
      case 'viewer':
        return 'bg-gray-100 text-gray-700 border-gray-200'
      default:
        return 'bg-gray-100 text-gray-700 border-gray-200'
    }
  }

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-gray-900">Current User</h2>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {users.map((user) => {
          const isSelected = user.username === currentUser
          return (
            <button
              key={user.username}
              onClick={() => onUserChange(user.username)}
              className={`p-4 rounded-lg border-2 transition-all ${
                isSelected
                  ? 'border-blue-600 bg-blue-50'
                  : 'border-gray-200 bg-white hover:border-gray-300'
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center space-x-2">
                  <User className="h-5 w-5 text-gray-600" />
                  <span className="font-medium text-gray-900">{user.username}</span>
                </div>
                {isSelected && (
                  <div className="h-2 w-2 bg-blue-600 rounded-full"></div>
                )}
              </div>
              <div className={`inline-flex items-center space-x-1 px-3 py-1 rounded-full text-xs font-medium border ${getRoleColor(user.role)}`}>
                {getRoleIcon(user.role)}
                <span className="capitalize">{user.role}</span>
              </div>
            </button>
          )
        })}
      </div>
    </div>
  )
}

export default UserSelector
