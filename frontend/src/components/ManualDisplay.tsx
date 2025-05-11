import React from 'react';

interface ManualDisplayProps {
  manual: string;
}

const ManualDisplay: React.FC<ManualDisplayProps> = ({ manual }) => (
  <div dangerouslySetInnerHTML={{ __html: manual }} />
);

export default ManualDisplay;