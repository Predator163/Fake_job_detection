import React, { useState } from 'react';
import './JobPostingForm.css';

const JobPostingForm = ({ onSubmit, loading }) => {
  const [formData, setFormData] = useState({
    title: '',
    location: '',
    department: '',
    salary_range: '',
    company_profile: '',
    description: '',
    requirements: '',
    benefits: '',
    telecommuting: 0,
    has_company_logo: 0,
    has_questions: 0,
    employment_type: '',
    required_experience: '',
    required_education: '',
    industry: '',
    function: ''
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? (checked ? 1 : 0) : value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="job-form">
      <h2>Enter Job Posting Details</h2>

      <div className="form-section">
        <h3>Basic Information</h3>
        
        <div className="form-group">
          <label htmlFor="title">Job Title *</label>
          <input
            type="text"
            id="title"
            name="title"
            value={formData.title}
            onChange={handleChange}
            placeholder="e.g., Senior Software Engineer"
            required
          />
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="location">Location</label>
            <input
              type="text"
              id="location"
              name="location"
              value={formData.location}
              onChange={handleChange}
              placeholder="e.g., New York, NY"
            />
          </div>

          <div className="form-group">
            <label htmlFor="department">Department</label>
            <input
              type="text"
              id="department"
              name="department"
              value={formData.department}
              onChange={handleChange}
              placeholder="e.g., Engineering"
            />
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="salary_range">Salary Range</label>
          <input
            type="text"
            id="salary_range"
            name="salary_range"
            value={formData.salary_range}
            onChange={handleChange}
            placeholder="e.g., $80,000 - $120,000"
          />
        </div>
      </div>

      <div className="form-section">
        <h3>Company & Job Details</h3>

        <div className="form-group">
          <label htmlFor="company_profile">Company Profile</label>
          <textarea
            id="company_profile"
            name="company_profile"
            value={formData.company_profile}
            onChange={handleChange}
            placeholder="Brief description of the company..."
            rows="3"
          />
        </div>

        <div className="form-group">
          <label htmlFor="description">Job Description *</label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            placeholder="Detailed job description..."
            rows="4"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="requirements">Requirements</label>
          <textarea
            id="requirements"
            name="requirements"
            value={formData.requirements}
            onChange={handleChange}
            placeholder="Job requirements and qualifications..."
            rows="4"
          />
        </div>

        <div className="form-group">
          <label htmlFor="benefits">Benefits</label>
          <textarea
            id="benefits"
            name="benefits"
            value={formData.benefits}
            onChange={handleChange}
            placeholder="Employee benefits..."
            rows="3"
          />
        </div>
      </div>

      <div className="form-section">
        <h3>Job Specifications</h3>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="employment_type">Employment Type</label>
            <select
              id="employment_type"
              name="employment_type"
              value={formData.employment_type}
              onChange={handleChange}
            >
              <option value="">Select...</option>
              <option value="Full-time">Full-time</option>
              <option value="Part-time">Part-time</option>
              <option value="Contract">Contract</option>
              <option value="Temporary">Temporary</option>
              <option value="Internship">Internship</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="required_experience">Required Experience</label>
            <select
              id="required_experience"
              name="required_experience"
              value={formData.required_experience}
              onChange={handleChange}
            >
              <option value="">Select...</option>
              <option value="Entry level">Entry level</option>
              <option value="Mid-Senior level">Mid-Senior level</option>
              <option value="Associate">Associate</option>
              <option value="Executive">Executive</option>
              <option value="Not Applicable">Not Applicable</option>
            </select>
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label htmlFor="required_education">Required Education</label>
            <select
              id="required_education"
              name="required_education"
              value={formData.required_education}
              onChange={handleChange}
            >
              <option value="">Select...</option>
              <option value="High School or equivalent">High School or equivalent</option>
              <option value="Bachelor's Degree">Bachelor's Degree</option>
              <option value="Master's Degree">Master's Degree</option>
              <option value="Doctorate">Doctorate</option>
              <option value="Unspecified">Unspecified</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="industry">Industry</label>
            <input
              type="text"
              id="industry"
              name="industry"
              value={formData.industry}
              onChange={handleChange}
              placeholder="e.g., Information Technology"
            />
          </div>
        </div>

        <div className="form-group">
          <label htmlFor="function">Function</label>
          <input
            type="text"
            id="function"
            name="function"
            value={formData.function}
            onChange={handleChange}
            placeholder="e.g., Engineering, Sales"
          />
        </div>
      </div>

      <div className="form-section">
        <h3>Additional Indicators</h3>

        <div className="checkbox-group">
          <label className="checkbox-label">
            <input
              type="checkbox"
              name="telecommuting"
              checked={formData.telecommuting === 1}
              onChange={handleChange}
            />
            <span>Telecommuting/Remote Work</span>
          </label>

          <label className="checkbox-label">
            <input
              type="checkbox"
              name="has_company_logo"
              checked={formData.has_company_logo === 1}
              onChange={handleChange}
            />
            <span>Has Company Logo</span>
          </label>

          <label className="checkbox-label">
            <input
              type="checkbox"
              name="has_questions"
              checked={formData.has_questions === 1}
              onChange={handleChange}
            />
            <span>Has Screening Questions</span>
          </label>
        </div>
      </div>

      <button 
        type="submit" 
        className="btn-submit"
        disabled={loading}
      >
        {loading ? 'Analyzing...' : 'Analyze Job Posting'}
      </button>
    </form>
  );
};

export default JobPostingForm;