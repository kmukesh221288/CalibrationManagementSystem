from services.dashboard_service import DashboardService

service = DashboardService()

data = service.get_counts()

print(data)

service.close()