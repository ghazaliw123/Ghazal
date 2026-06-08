import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
import json
import sys

def load_metrics(filename='metrics.json'):
    """بارگذاری اطلاعات ذخیره شده"""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except:
        print(f"❌ فایل {filename} پیدا نشد")
        return None

def plot_metrics(data):
    """رسم نمودار"""
    if not data:
        return
    
    timestamps = data['timestamp']
    cpu = data['cpu_usage']
    memory = data['memory_usage']
    total_requests = data['total_requests']
    
    # ایجاد نمودارها
    fig, axes = plt.subplots(2, 1, figsize=(14, 9))
    fig.suptitle('تاثیر حملۀ DDoS بر عملکرد سرور', fontsize=18, fontweight='bold')
    
    # نمودار CPU
    axes[0].plot(range(len(cpu)), cpu, color='red', linewidth=2.5, label='مصرف CPU')
    axes[0].fill_between(range(len(cpu)), cpu, alpha=0.3, color='red')
    axes[0].set_ylabel('مصرف CPU (%)', fontsize=12, fontweight='bold')
    axes[0].set_title('مصرف CPU قبل، حین و بعد از حمله', fontsize=13, fontweight='bold')
    axes[0].grid(True, alpha=0.3, linestyle='--')
    axes[0].legend(fontsize=11)
    axes[0].set_ylim(0, 100)
    
    # افزودن متن اطلاعاتی
    avg_cpu = sum(cpu) / len(cpu)
    max_cpu = max(cpu)
    axes[0].text(0.02, 0.95, f'میانگین CPU: {avg_cpu:.1f}%\nحداکثر CPU: {max_cpu:.1f}%', 
                transform=axes[0].transAxes, fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # نمودار Memory
    axes[1].plot(range(len(memory)), memory, color='blue', linewidth=2.5, label='مصرف حافظه')
    axes[1].fill_between(range(len(memory)), memory, alpha=0.3, color='blue')
    axes[1].set_xlabel('زمان (ثانیه)', fontsize=12, fontweight='bold')
    axes[1].set_ylabel('مصرف حافظه (%)', fontsize=12, fontweight='bold')
    axes[1].set_title('مصرف حافظه قبل، حین و بعد از حمله', fontsize=13, fontweight='bold')
    axes[1].grid(True, alpha=0.3, linestyle='--')
    axes[1].legend(fontsize=11)
    axes[1].set_ylim(0, 100)
    
    # افزودن متن اطلاعاتی
    avg_mem = sum(memory) / len(memory)
    max_mem = max(memory)
    axes[1].text(0.02, 0.95, f'میانگین حافظه: {avg_mem:.1f}%\nحداکثر حافظه: {max_mem:.1f}%\nکل درخواست‌ها: {total_requests}', 
                transform=axes[1].transAxes, fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig('ddos_analysis.png', dpi=150, bbox_inches='tight')
    print('✅ نمودار در فایل ddos_analysis.png ذخیره شد')
    plt.show()

if __name__ == '__main__':
    data = load_metrics()
    plot_metrics(data)