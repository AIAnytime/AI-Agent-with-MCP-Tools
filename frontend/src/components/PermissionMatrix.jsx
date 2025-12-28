import React, { useState, useEffect } from 'react'
import { Check, X, Shield } from 'lucide-react'
import { fetchPermissions } from '../api/api'

function PermissionMatrix({ users }) {
  const [permissions, setPermissions] = useState({})

  useEffect(() => {
    loadPermissions()
  }, [users])

  const loadPermissions = async () => {
    const perms = {}
    for (const user of users) {
      try {
        const data = await fetchPermissions(user.role)
        perms[user.role] = data.permissions || []
      } catch (error) {
        console.error(`Failed to load permissions for ${user.role}:`, error)
      }
    }
    setPermissions(perms)
  }

  const actions = ['create', 'read', 'update', 'delete']
  const roles = ['admin', 'editor', 'viewer']

  const hasPermission = (role, action) => {
    const rolePerms = permissions[role] || []
    return rolePerms.some(p => p.action === action && p.resource === 'document')
  }

  const getRoleColor = (role) => {
    switch (role) {
      case 'admin':
        return 'bg-purple-100 text-purple-700'
      case 'editor':
        return 'bg-blue-100 text-blue-700'
      case 'viewer':
        return 'bg-gray-100 text-gray-700'
      default:
        return 'bg-gray-100 text-gray-700'
    }
  }

  return (
    <div>
      <div className="flex items-center space-x-3 mb-6">
        <Shield className="h-6 w-6 text-blue-600" />
        <h2 className="text-xl font-semibold text-gray-900">Permission Matrix (RBAC)</h2>
      </div>

      <div className="bg-gray-50 rounded-lg p-6 mb-6">
        <h3 className="text-sm font-medium text-gray-700 mb-2">About RBAC</h3>
        <p className="text-sm text-gray-600">
          Role-Based Access Control (RBAC) is enforced using PyCasbin. Each role has specific permissions
          for document operations. The AI Agent checks these permissions before executing any action.
        </p>
      </div>

      <div className="overflow-hidden border border-gray-200 rounded-lg">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-4 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">
                Role / User
              </th>
              {actions.map((action) => (
                <th
                  key={action}
                  className="px-6 py-4 text-center text-xs font-semibold text-gray-700 uppercase tracking-wider"
                >
                  {action}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {roles.map((role) => {
              const roleUsers = users.filter(u => u.role === role).map(u => u.username)
              return (
                <tr key={role} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div>
                      <div className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium ${getRoleColor(role)}`}>
                        <span className="capitalize">{role}</span>
                      </div>
                      {roleUsers.length > 0 && (
                        <div className="text-xs text-gray-500 mt-1">
                          {roleUsers.join(', ')}
                        </div>
                      )}
                    </div>
                  </td>
                  {actions.map((action) => {
                    const allowed = hasPermission(role, action)
                    return (
                      <td key={action} className="px-6 py-4 text-center">
                        {allowed ? (
                          <div className="inline-flex items-center justify-center h-8 w-8 rounded-full bg-green-100">
                            <Check className="h-5 w-5 text-green-600" />
                          </div>
                        ) : (
                          <div className="inline-flex items-center justify-center h-8 w-8 rounded-full bg-red-100">
                            <X className="h-5 w-5 text-red-600" />
                          </div>
                        )}
                      </td>
                    )
                  })}
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>

      <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
          <h4 className="font-semibold text-purple-900 mb-2">Admin Role</h4>
          <p className="text-sm text-purple-700">Full access to all operations including delete</p>
        </div>
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <h4 className="font-semibold text-blue-900 mb-2">Editor Role</h4>
          <p className="text-sm text-blue-700">Can create, read, and update documents but cannot delete</p>
        </div>
        <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
          <h4 className="font-semibold text-gray-900 mb-2">Viewer Role</h4>
          <p className="text-sm text-gray-700">Read-only access to documents</p>
        </div>
      </div>
    </div>
  )
}

export default PermissionMatrix
