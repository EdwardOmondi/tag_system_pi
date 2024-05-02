export type PiResponse = {
  scanner_id: string;
  bracelet_id: string;
  status: 'INITIAL_SCAN' | 'SCAN_COMPLETE' | 'TOO_SOON'|'INITIAL_CONNECTION';
  response: string;
};
export type Data = {
  scannerId: string;
  braceletId: string;
  timestamp: number;
};

export type CloudResponse = {
  Result: number;
  Message: string;
  data: RequestResponse | null;
};

type RequestResponse = {
  user: User;
  scanner: Scanner;
  bracelets: Bracelets;
};

type User = {
  id: string;
  name: string;
  email: string;
};

type Scanner = {
  id: string;
  name: string;
  points: string;
};

type Bracelets = {
  id: string;
  name: string;
  bracelet_type: string;
};
