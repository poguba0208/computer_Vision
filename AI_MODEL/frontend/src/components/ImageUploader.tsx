import { useRef, useState, useCallback } from "react";

interface Props {
  onUpload: (file: File) => void;
  isLoading: boolean;
}

export default function ImageUploader({ onUpload, isLoading }: Props) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [isDragging, setIsDragging] = useState(false);

  const handleFile = (file: File) => {
    if (!file.type.startsWith("image/")) {
      alert("이미지 파일만 업로드 가능합니다.");
      return;
    }
    onUpload(file);
  };

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setIsDragging(false);
      if (isLoading) return;
      const file = e.dataTransfer.files[0];
      if (file) handleFile(file);
    },
    [isLoading]
  );

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) handleFile(file);
    e.target.value = "";
  };

  return (
    <div
      className={`uploader ${isDragging ? "dragging" : ""}`}
      onDragOver={(e) => {
        e.preventDefault();
        setIsDragging(true);
      }}
      onDragLeave={() => setIsDragging(false)}
      onDrop={handleDrop}
      onClick={() => !isLoading && inputRef.current?.click()}
    >
      <input
        ref={inputRef}
        type="file"
        accept="image/*"
        onChange={handleChange}
        hidden
      />
      {isLoading ? (
        <div className="upload-content">
          <div className="spinner" />
          <p>분석 중...</p>
        </div>
      ) : (
        <div className="upload-content">
          <div className="upload-icon">+</div>
          <p>이미지를 드래그하거나 클릭하여 업로드</p>
          <span className="upload-hint">JPG, PNG, BMP, WebP (최대 10MB)</span>
        </div>
      )}
    </div>
  );
}
