export type PiResponse = {
  scanner_id: string;
  bracelet_id: string;
  status:
    | 'INITIAL_CONNECTION'
    | 'INITIAL_SCAN'
    | 'TOO_SOON'
    | 'SCAN_COMPLETE'
    | 'DISCONNECTED';
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
  data: RequestResponse;
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
