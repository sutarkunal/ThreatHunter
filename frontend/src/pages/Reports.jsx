/**
 * Reports Page - Generate and view incident reports
 */
import { FileText, Download } from 'lucide-react';
import Card from '../components/common/Card';

export default function Reports() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Reports</h1>
        <p className="text-gray-600 mt-1">Generate and download incident reports</p>
      </div>

      {/* Coming Soon */}
      <Card>
        <div className="text-center py-16">
          <FileText className="w-20 h-20 text-gray-400 mx-auto mb-6" />
          <h2 className="text-2xl font-bold text-gray-700 mb-3">Report Generation Coming Soon</h2>
          <p className="text-gray-600 mb-6 max-w-md mx-auto">
            This feature will allow you to generate comprehensive incident reports including:
          </p>

          <div className="max-w-lg mx-auto text-left space-y-3 mb-8">
            <div className="flex items-start space-x-3">
              <div className="w-2 h-2 bg-primary-500 rounded-full mt-2" />
              <p className="text-gray-700">Executive summary of detected threats</p>
            </div>
            <div className="flex items-start space-x-3">
              <div className="w-2 h-2 bg-primary-500 rounded-full mt-2" />
              <p className="text-gray-700">Detailed alert breakdown by severity and type</p>
            </div>
            <div className="flex items-start space-x-3">
              <div className="w-2 h-2 bg-primary-500 rounded-full mt-2" />
              <p className="text-gray-700">Top suspicious IPs and connection patterns</p>
            </div>
            <div className="flex items-start space-x-3">
              <div className="w-2 h-2 bg-primary-500 rounded-full mt-2" />
              <p className="text-gray-700">Traffic analysis and protocol statistics</p>
            </div>
            <div className="flex items-start space-x-3">
              <div className="w-2 h-2 bg-primary-500 rounded-full mt-2" />
              <p className="text-gray-700">Export to PDF and JSON formats</p>
            </div>
          </div>

          <div className="inline-flex items-center space-x-2 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg">
            <Download className="w-4 h-4" />
            <span className="text-sm font-medium">Available in Phase 4</span>
          </div>
        </div>
      </Card>
    </div>
  );
}
