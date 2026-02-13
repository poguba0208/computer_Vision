export interface DetectionDetail {
  class: "head" | "helmet" | string;
  confidence: number;
  bbox: [number, number, number, number]; // [x1, y1, x2, y2]
}

export type SafetyStatus = "Safe" | "Warning" | "Danger" | "Error";

export interface DetectionResult {
  success: boolean;
  image_url: string;
  image_width: number;
  image_height: number;
  summary: {
    total_workers: number;
    helmet_worn: number;
    helmet_not_worn: number;
    risk_percentage: number;
    safety_status: SafetyStatus;
  };
  details: DetectionDetail[];
}
